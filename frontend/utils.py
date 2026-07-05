"""Small shared helpers used across frontend components."""
 
 
def year_of(date_str: str) -> int:
    """Meeting dates are stored as 'YYYY_MM_DD'."""
    return int(date_str.split("_")[0])
 