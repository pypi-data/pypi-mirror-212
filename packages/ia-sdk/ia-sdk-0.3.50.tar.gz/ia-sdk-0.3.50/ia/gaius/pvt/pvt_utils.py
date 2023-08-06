"""Utilities for PVT computations"""
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from numpy import nan
from copy import deepcopy
import math
from pathlib import Path

def init_emotive_on_node(emotive: str, node: str, test_step_info: dict):
    """Helper function to initialize emotive information for live messages.
    Used if new emotive is encountered during testing
    (emotive only seen in specific records, not consistently across all)

    Args:
        emotive (str): emotive name
        node (str): node to initialize emotive on
        test_step_info (dict): dictionary of live information, which should
            be initialized with new emotive
    """
    test_step_info['overall']['response_counts'][node][emotive] = 0
    test_step_info['overall']['true_positive'][node][emotive] = 0
    test_step_info['overall']['true_negative'][node][emotive] = 0
    test_step_info['overall']['false_positive'][node][emotive] = 0
    test_step_info['overall']['false_negative'][node][emotive] = 0
    test_step_info['overall']['testing_counter'][node][emotive] = 0
    
    # init positive and negative metrics
    test_step_info['positive']['response_counts'][node][emotive] = 0
    test_step_info['positive']['true_positive'][node][emotive] = 0
    test_step_info['positive']['true_negative'][node][emotive] = 0
    test_step_info['positive']['false_positive'][node][emotive] = 0
    test_step_info['positive']['false_negative'][node][emotive] = 0
    test_step_info['positive']['testing_counter'][node][emotive] = 0
    
    test_step_info['negative']['response_counts'][node][emotive] = 0
    test_step_info['negative']['true_positive'][node][emotive] = 0
    test_step_info['negative']['true_negative'][node][emotive] = 0
    test_step_info['negative']['false_positive'][node][emotive] = 0
    test_step_info['negative']['false_negative'][node][emotive] = 0
    test_step_info['negative']['testing_counter'][node][emotive] = 0
    return

def compute_residual(predicted: float, actual: float) -> float:
    """Compute residual given predicted and actual

    Args:
        predicted (float): predicted emotive value
        actual (float): actual emotive value
    """
    
    return (actual - predicted)
    
def compute_abs_residual(predicted: float, actual: float):
    """Compute absolute residual

    Args:
        predicted (float): predicted emotive value
        actual (float): actual emotive value
    """
    return abs(actual - predicted)

def compute_squared_residual(predicted: float, actual: float):
    """Compute absolute residual

    Args:
        predicted (float): predicted emotive value
        actual (float): actual emotive value
    """
    return math.pow(actual - predicted, 2)

def smape(previous_smape: float, count: int, abs_residual: float, predicted: float, actual: float):
    """Computes the new SMAPE, given previous smape,count, predicted and actual value

    Args:
        count (int): Response count for specific emotive on node
        predicted (float): predicted emotive value
        actual (float): actual emotive value
        previous_smape (float): Previous smape.
    """
    return 100 * ((((previous_smape / 100) * count) + ((2 * abs_residual) / (abs(predicted) + abs(actual)))) / (count + 1))

def rmse(previous_rmse: float, count: int, squared_residual: float):
    """Compute new RMSE given previous RMSE value, count, and new squared residual

    Args:
        previous_rmse (float): previous RMSE value
        count (int): Response count for specific emotive on node
        squared_residual (float): current squared residual value
    """
    return math.sqrt(((math.pow(previous_rmse, 2) * count) + squared_residual) / (count + 1))

def f1_score(tp: int, fp: int, fn: int):
    """Compute F1 Score

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
        fn (int): False Negative count
    """
    f1 = 0.0
    try:
        f1 = (2 * tp) / ((2 * tp) + fp + fn)
    except ZeroDivisionError:
        pass
    return f1

def false_discovery_rate(tp: int, fp: int):
    """Compute FDR

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
    """
    fdr = 0.0
    try:
        fdr = fp / (fp + tp)
    except ZeroDivisionError:
        pass
    return fdr

def true_negative_rate(tn: int, fp: int):
    """Compute FDR

    Args:
        tn (int): True Negative count
        fp (int): False Positive count
    """
    tnr = 0.0
    try:
        tnr = tn / (tn + fp)
    except ZeroDivisionError:
        pass
    return tnr

def true_positive_rate(tp: int, fn: int):
    """Compute FDR

    Args:
        tp (int): True Positive count
        fn (int): False Negative count
    """
    tpr = 0.0
    try:
        tpr = tp / (tp + fn)
    except ZeroDivisionError:
        pass
    return tpr

def negative_predictive_value(tn: int, fn: int):
    """Compute NPV

    Args:
        tn (int): True Negative count
        fn (int): False Negative count
    """
    npv = 0.0
    try:
        npv = tn / (tn + fn)
    except ZeroDivisionError:
        pass
    return npv 

def false_negative_rate(fn: int, tp: int):
    """Compute FNR

    Args:
        fn (int): False Negative count
        tp (int): True Positive count
    """
    fnr = 0.0
    try:
        fnr = fn / (fn + tp)
    except ZeroDivisionError:
        pass
    return fnr 

def false_omission_rate(fn: int, tn: int):
    """Compute FOR

    Args:
        fn (int): False Negative count
        tn (int): True Negative count
    """
    false_or = 0.0
    try:
        false_or = fn / (fn + tn)
    except ZeroDivisionError:
        pass
    return false_or 

def false_positive_rate(fp: int, tn: int):
    """Compute FPR

    Args:
        fp (int): False Positive count
        tn (int): True Negative count
    """
    fpr = 0.0
    try:
        fpr = fp / (fp + tn)
    except ZeroDivisionError:
        pass
    return fpr

def positive_likelihood_ratio(tp: int, fp: int, tn: int, fn: int):
    """Compute LR+

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
        tn (int): True Negative count
        fn (int): False Negative count
    """
    lr_plus = 0.0
    try:
        lr_plus = true_positive_rate(tp=tp, fn=fn) / false_positive_rate(fp=fp, tn=tn)
    except ZeroDivisionError:
        pass
    return lr_plus 

def negative_likelihood_ratio(tp: int, fp: int, tn: int, fn: int):
    """Compute LR-

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
        tn (int): True Negative count
        fn (int): False Negative count
    """
    lr_minus = 0.0
    try:
        lr_minus = false_negative_rate(fn=fn, tp=tp) / true_negative_rate(tn=tn, fp=fp)
    except ZeroDivisionError:
        pass
    return lr_minus

def prevalence_threshold(tp: int, fp: int, tn: int, fn: int):
    """Compute PT

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
        tn (int): True Negative count
        fn (int): False Negative count
    """
    pt = 0.0
    try:
        pt = math.sqrt(false_positive_rate(fp=fp, tn=tn)) / (math.sqrt(true_positive_rate(tp=tp, fn=fn)) + math.sqrt(false_positive_rate(fp=fp, tn=tn)))
    except ZeroDivisionError:
        pass
    return pt

def threat_score(tp: int, fp: int, fn: int):
    """Compute TS

    Args:
        tp (int): True Positive count
        fp (int): False Positive count
        fn (int): False Negative count
    """
    ts = 0.0
    try:
        ts = tp / (tp + fn + fp)
    except ZeroDivisionError:
        pass
    return ts

def update_accuracy(tp: int, tn: int, overall_count: int) -> float:
    """Update accuracy metrics

    Args:
        tp (int): True Positives
        tn (int): True Negatives
        overall_count (int): current testing record count

    Returns:
        float: accuracy
    """
    accuracy = 0.0
    try:
        accuracy = 100.0 * (tp + tn) / overall_count
    except ZeroDivisionError:
        pass
    return accuracy

def update_precision(tp: int, tn: int, response_count: int) -> float:
    """Update precision metrics

    Args:
        tp (int): True Positives
        tn (int): True Negatives
        response_count (int): node response count

    Returns:
        float: precision
    """
    precision = 0.0
    try:
        precision = 100.0 * (tp + tn) / response_count
    except ZeroDivisionError:
        pass
    return precision

def plot_confusion_matrix(test_num: int, class_metrics_data_structures: dict, QUIET: bool, results_dir=None):
    """
    Takes a node classification test to create a confusion matrix.
    This version includes the i_dont_know or unknown label.
    """

    for node_name, class_metrics_data in class_metrics_data_structures.items():
        # print(f'-------------Test#{test_num}-{node_name}-Plots-------------')
        sorted_labels = deepcopy(class_metrics_data['labels'])
        sorted_labels = [str(label) for label in sorted_labels if label is not None]
        sorted_labels.append(str(None))
        # sorted_labels = sorted(class_metrics_data['labels'])
        actuals = [[str(elem) for elem in act] for act in class_metrics_data['actuals']]
        preds = [str(pred) for pred in class_metrics_data['predictions']]
        cm = confusion_matrix(actuals, #TODO: each "actual" is a list, to support multiclass labels. Need to find solution here
                              preds,
                              labels=sorted_labels)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                      display_labels=sorted_labels)
        
        disp.plot()
        disp.ax_.set_title(f'Test#{test_num}-{node_name} Confusion Matrix')
        current_figure = plt.gcf()
        if is_notebook() and not QUIET:
            plt.show()
        if results_dir is not None:
            cf_filename = Path(results_dir).joinpath(f'./confusion_matrix_{node_name}_test_{test_num}.png')
            # cf_filename = f'./confusion_matrix_{node_name}_test_{test_num}.png'
            # print(f'attempting to save confusion_matrix to: {cf_filename}')
            try:
                current_figure.savefig(cf_filename)
            except Exception as e:
                print(f'error saving confusion matrix to {cf_filename}: {str(e)}')
        plt.close()


def is_notebook() -> bool: # pragma: no cover (helper function to determine if we are in a jupyter notebook)
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
