import wml.visionml as wv

__all__ = ['site_date_res']


def site_date_res(site_id= 30607):
    """
    Get the site date report closure data
    Args:
        site_id : Site id for fetching the date wise result. Site_id : 30607 (Waldof)
    
    Returns:
        pd.DateFrame
    """
    q1 = """
    select s.start_date,s.id,s.meal_service_state, s.closed from pp_meal_service.view_current_state cs
               join pp_meal_service.view_service s on s.view_current_state_id = cs.id
		       where cs.site_id = {} 
               """.format(site_id)
    return wv.read_sql(q1,wv.ml_engine)