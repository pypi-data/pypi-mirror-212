# Copyright (C) 2023-Present DAGWorks Inc.
#
# For full terms email support@dagworks.io.
#
# This software and associated documentation files (the "Software") may only be
# used in production, if you (and any entity that you represent) have agreed to,
# and are in compliance with, the DAGWorks Enterprise Terms of Service, available
# via email (support@dagworks.io) (the "Enterprise Terms"), or other
# agreement governing the use of the Software, as agreed by you and DAGWorks,
# and otherwise have a valid DAGWorks Enterprise license for the
# correct number of seats and usage volume.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import functools
import json
import logging
import sys
import time as py_time
import traceback
from contextlib import contextmanager
from datetime import datetime, time
from typing import Any, Callable, Dict, List, Union

import pandas as pd
from hamilton import base
from hamilton import node as h_node
from hamilton.data_quality import base as dq_base
from packaging.version import Version

from dagworks.tracking.trackingtypes import DAGRun, Status, TaskRun

try:
    import polars as pl

    has_polars = True
except ImportError:
    has_polars = False


logger = logging.getLogger(__name__)


def compute_polars_stats(
    result: Union["pl.DataFrame", "pl.Series"], node: h_node.Node
) -> Dict[str, Any]:
    """Computes data observability stats for polars. Mirrors pandas (as much as possible).

    :param result: the result to compute data observability stats for
    :param node: the node that produced the result
    :return: dict of data observability stats -- different if series or dataframe passed in.
    """
    _temp = result.describe().to_pandas()
    if "statistic" in _temp.columns:
        _temp.index = _temp.statistic
        del _temp["statistic"]
    else:
        _temp.index = _temp["describe"]
        del _temp["describe"]
    pl_describe = json.loads(_temp.to_json())
    if isinstance(result, pl.Series):
        pl_describe = pl_describe["value"]
        pl_describe["dtype"] = str(result.dtype)
        pl_describe["25%"] = pl_describe.get("25%", None)
        pl_describe["50%"] = pl_describe["median"]
        pl_describe["75%"] = pl_describe.get("75%", None)
        pl_describe["std"] = pl_describe.get("std", None)
        pl_describe["count"] = int(int(pl_describe["count"]) - int(pl_describe["null_count"]))
        del pl_describe["null_count"]
        del pl_describe["median"]
        pl_describe = {
            node.name: pl_describe
        }  # wrap series to make it look like a dataframe describe output dict.
    else:
        for col in result.columns:
            if col in pl_describe:
                pl_describe[col]["dtype"] = str(result[col].dtype)
                pl_describe[col]["25%"] = pl_describe[col].get("25%", None)
                pl_describe[col]["50%"] = pl_describe[col]["median"]
                pl_describe[col]["75%"] = pl_describe[col].get("75%", None)
                pl_describe[col]["std"] = pl_describe[col].get("std", None)
                pl_describe[col]["count"] = int(
                    int(pl_describe[col]["count"]) - int(pl_describe[col]["null_count"])
                )
                del pl_describe[col]["null_count"]
                del pl_describe[col]["median"]
            else:
                pl_describe[col] = {"dtype": str(result[col].dtype)}
    return pl_describe


def compute_pandas_stats(
    result: Union[pd.DataFrame, pd.Series], node: h_node.Node
) -> Dict[str, Any]:
    """Computes stats for pandas.

    :param result:  the result to compute data observability stats for
    :param node:    the node that produced the result
    :return:    dict of data observability stats -- different if series or dataframe passed in.
    """
    kwargs = {} if Version(pd.__version__) > Version("1.5") else {"datetime_is_numeric": True}
    pd_describe = json.loads(result.describe(include="all", **kwargs).to_json())
    if isinstance(result, pd.Series):
        pd_describe["dtype"] = str(result.dtype)
        pd_describe = {
            node.name: pd_describe
        }  # wrap series to make it look like a dataframe describe output dict.
    else:
        for col in result.columns:
            if col in pd_describe:
                pd_describe[col]["dtype"] = str(result[col].dtype)
            else:
                pd_describe[col] = {"dtype": str(result[col].dtype)}
    return pd_describe


def process_result(result: Any, node: h_node.Node) -> Any:
    """Processes result -- this is purely a by-type mapping.
    Note that this doesn't actually do anything yet -- the idea is that we can return DQ
    results, and do other stuff with other results -- E.G. summary stats on dataframes,
    pass small strings through, etc...

    The return type is left as Any for now, but we should probably make it a union of
    types that we support.

    Note this should keep the cardinality of the output as low as possible.
    These results will be used on the FE to display results, and we don't want
    to crowd out storage.

    :param result: The result of the node's execution
    :param node: The node that produced the result
    :return: The processed  result - it has to be JSON serializable!
    """

    try:
        # introspect the result...
        if isinstance(result, (pd.DataFrame, pd.Series)):
            # do something quick and dirty here for pandas -- will likely need to add geopandas
            # equivalents to describe() isn't complete -- so it could miss some dtypes.
            start = py_time.time()
            pd_describe = compute_pandas_stats(result, node)
            end = py_time.time()
            logger.debug(f"Took {end - start} seconds to describe dataframe/series: {node.name}")
            return {
                "observability_type": "pandas_describe",
                "observability_value": pd_describe,
                # expect other describes, or we standardize the structure (could go TFX DV route).
                "observability_schema_version": "0.0.1",
            }
        elif isinstance(result, (str, int, float, bool)):
            return {
                "observability_type": "primitive",
                "observability_value": {
                    "type": str(type(result)),
                    "value": result,
                },
                "observability_schema_version": "0.0.1",
            }
        elif has_polars and isinstance(result, (pl.DataFrame, pl.Series)):
            pl_describe = compute_polars_stats(result, node)
            return {
                "observability_type": "pandas_describe",
                "observability_value": pl_describe,
                # expect other describes, or we standardize the structure (could go TFX DV route).
                "observability_schema_version": "0.0.1",
            }
        return {
            "observability_type": "unsupported",
            "observability_value": {
                "unsupported_type": str(type(result)),
                "action": "reach out to the DAGWorks team to add support for this type.",
            },
            "observability_schema_version": "0.0.1",
        }
    # TODO: introspect other nodes
    # if it's a check_output node, then we want to process the pandera result/the result from it.
    except Exception as e:
        logger.warning(f"Failed to introspect result for {node.name}. Error:\n{e}")


# This will be needed for later as we send information over to the server
# For now this is commented out


class TrackingState:
    """Mutable class that tracks data"""

    def __init__(self, run_id: str):
        """Initializes the tracking state"""
        self.status = Status.UNINITIALIZED
        self.start_time = None
        self.run_id = run_id
        self.task_map: Dict[str, TaskRun] = {}
        self.update_status(Status.UNINITIALIZED)

    def clock_start(self):
        """Called at start of run"""
        logger.info("Clocked beginning of run")
        self.status = Status.RUNNING
        self.start_time = datetime.now()

    def clock_end(self, status: Status):
        """Called at end of run"""
        logger.info(f"Clocked end of run with status: {status}")
        self.end_time = datetime.now()
        self.status = status

    def update_task(self, task_name: str, task_run: TaskRun):
        """Updates a task"""
        self.task_map.update({task_name: task_run})
        logger.debug(f"Updating task: {task_name} with data: {task_run}")

    def update_status(self, status: Status):
        """Updates the status of the run"""
        self.status = status
        logger.info(f"Updating run status with value: {status}")

    def get(self) -> DAGRun:
        """Gives the final result as a DAG run"""
        return DAGRun(
            run_id=self.run_id,
            status=self.status,
            # TODO -- think about using a json dumper and referring to this as a status
            tasks=list(self.task_map.values()),
            start_time=self.start_time,
            end_time=self.end_time,
            schema_version=0,
        )


def serialize_error() -> List[str]:
    """Serialize an error to a string.
    Note we should probably have this *unparsed*, so we can display in the UI,
    but its OK for now to just have the string.

    *note* this has to be called from within an except block.

    :param error:
    :return:
    """
    exc_type, exc_value, exc_tb = sys.exc_info()
    return traceback.format_exception(exc_type, exc_value, exc_tb)


def serialize_data_quality_error(e: dq_base.DataValidationError) -> List[str]:
    """Santizes data quality errors to make them more readable for the platform.

    Note: this is hacky code.

    :param e: Data quality error to inspect
    :return: list of failures.
    """
    validation_failures = e.args[0]
    sanitized_failures = []
    for failure in validation_failures:
        if "pandera_schema_validator" in failure:  # hack to know what type of validator.
            sanitized_failures.append(failure.split("Usage Tip")[0])  # remove usage tip
        else:
            sanitized_failures.append(failure)
    return sanitized_failures


class RunTracker:
    """This class allows you to track results of runs"""

    def __init__(self, tracking_state: TrackingState):
        """Tracks runs given run IDs. Note that this needs to be re-initialized
        on each run, we'll want to fix that.

        :param result_builder: Result builder to use
        :param run_id: Run ID to save with
        """
        self.tracking_state = tracking_state

    def execute_node(
        self,
        original_execute_node: Callable[[h_node.Node, Dict[str, Any]], Any],
        node: h_node.Node,
        kwargs: Dict[str, Any],
    ) -> Any:
        """Given a node that represents a hamilton function, execute it.
        Note, in some adapters this might just return some type of "future".

        :param node: the Hamilton Node
        :param kwargs: the kwargs required to exercise the node function.
        :return: the result of exercising the node.
        :param original_execute_node: The original adapter's callable
        """
        logger.debug(f"Executing node: {node.name}")
        # If the hamilton_tracking state hasn't started
        if self.tracking_state.status == Status.UNINITIALIZED:
            self.tracking_state.update_status(Status.RUNNING)

        task_run = TaskRun(node_name=node.name)  # node run.
        task_run.status = Status.RUNNING
        task_run.start_time = datetime.now()
        self.tracking_state.update_task(node.name, task_run)
        try:
            result = original_execute_node(node, kwargs)
            task_run.status = Status.SUCCESS
            task_run.result_type = type(result)
            task_run.result_summary = process_result(result, node)  # add node
            task_run.end_time = datetime.now()
            self.tracking_state.update_task(node.name, task_run)
            logger.debug(f"Node: {node.name} ran successfully")
            return result
        except dq_base.DataValidationError as e:
            task_run.status = Status.FAILURE
            task_run.end_time = datetime.now()
            task_run.error = serialize_data_quality_error(e)
            self.tracking_state.update_status(Status.FAILURE)
            self.tracking_state.update_task(node.name, task_run)
            logger.debug(f"Node: {node.name} encountered data quality issue...")
            raise e
        except Exception as e:
            task_run.status = Status.FAILURE
            task_run.end_time = datetime.now()
            task_run.error = serialize_error()
            self.tracking_state.update_status(Status.FAILURE)
            self.tracking_state.update_task(node.name, task_run)
            logger.debug(f"Node: {node.name} failed to run...")
            raise e


@contextmanager
def monkey_patch_adapter(adapter: base.HamiltonGraphAdapter, tracking_state: TrackingState):
    """Monkey patches the graph adapter to track the results o fthe run

    :param adapter: Adapter to modify the execute_node functionality
    :param tracking_state: State of the DAG -- used for tracking
    """
    old_execute_node = adapter.execute_node
    try:
        run_tracker = RunTracker(tracking_state=tracking_state)
        # monkey patch the adapter
        adapter.execute_node = functools.partial(run_tracker.execute_node, old_execute_node)
        yield
    finally:
        adapter.execute_node = old_execute_node
