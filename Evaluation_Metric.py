from typing import Optional
import re
  
def modified_modified_relaxed_accuracy(question:str,
                        target: str,
                        prediction: str,
                        max_relative_change: float = 0.05) -> bool:

  def _to_float(text: str) -> Optional[float]:
    try:
      if text.endswith("%"):
        return float(text.rstrip("%")) / 100.0
      else:
        return float(text)
    except ValueError:
      return None
    
  def _remove_commas_from_numbers(text: str) -> str:
    text = re.sub(r'(\d*),(\d+)', r'\1\2', text)
    return text
  
  def _remove_spaces(text: str) -> str:
    return text.replace(" ", "")
  
  def _check_for_years(question: str) -> bool:
    return "year" in question.lower()
  
  def _check_list(text: str) -> bool:
    return text.startswith("[") and text.endswith("]")
  
  def _list_of_answers(target: str, prediction: str) -> bool:
    target = target.split(",")
    prediction = prediction.split(",")
    target = sorted(target)
    prediction = sorted(prediction)
    return target == prediction
  
  prediction = _remove_commas_from_numbers(prediction)
  target = _remove_commas_from_numbers(target)
  
  prediction_float = _to_float(prediction)
  target_float = _to_float(target)
  
  if not _check_for_years(question) and (prediction_float is not None and target_float is not None):
    try :
      relative_change = abs(prediction_float - target_float) / abs(target_float)
      return relative_change <= max_relative_change
    except :
      return False
  else:
    prediction = _remove_spaces(prediction)
    target = _remove_spaces(target)
    
    if _check_list(target) and _check_list(prediction):
      return _list_of_answers(target[1:-1], prediction[1:-1])
    elif _check_list(target) or _check_list(prediction):
        return _list_of_answers(target[1:-1], prediction) or _list_of_answers(target, prediction[1:-1])
    else:
      return target.lower() in prediction.lower() or (prediction.lower() in target.lower() and len(prediction) > 0)