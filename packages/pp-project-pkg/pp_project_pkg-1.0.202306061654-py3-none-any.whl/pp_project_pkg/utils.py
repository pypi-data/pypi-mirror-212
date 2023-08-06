import wml.visionml as wv
import datetime
import mb.pandas as pd

__all__ = ['site_date_res','check_if_valid_date']


def site_date_res(site_id= 30607):
    """
    Get the site date report closure data
    Args:
        site_id : Site id for fetching the date wise result. Site_id : 30607 (Waldof)
    
    Returns:
        pd.DateFrame
    """
    q1 = """
    select s.start_date,s.id,s.meal_service_state, s.closed,s.updated from pp_meal_service.view_current_state cs
               join pp_meal_service.view_service s on s.view_current_state_id = cs.id
		       where cs.site_id = {} 
               """.format(site_id)
    return wv.read_sql(q1,wv.ml_engine)

def check_if_valid_date(site_res, date):
    """
    Check if the date (str) has closed the report.

    Args:
        site_res: complete report of the site_data_res
        date: string value of date. format : '2023-06-06'
    
    Output:
        Bool
    """

    k =datetime.datetime.strptime(date,'%Y-%m-%d').date()
    l = site_res[site_res['start_date']==k]
    
    l_d = l['closed'].iloc[0]
    
    if pd.isnull(l_d):
        return False
    
    if  (l_d).to_pydatetime().date() < k:
        return False
    
    return True