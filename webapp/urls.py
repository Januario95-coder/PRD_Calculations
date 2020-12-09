from django.urls import path
from .views import (
    main_page,
    login_page,
    logout_page,
    create_prd,
    homepage,
    prd_input_data,
    inspection_planning,
    risk_assessment,
    prd_insp_history,
    applicable_overpres_demand_case,

    delete_inspe_history_obj,
    delete_applic_overpr_obj
)


app_name = 'webapp'


urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('main_page/', main_page, name='main_page'),
    path('create_prd/', create_prd, name='create_prd'),
    # path('', homepage, name='homepage'),
    # path('input_data/', prd_input_data, name='input_data'),
    # path('inspection_planning/', inspection_planning,
    #      name='inspection_planning'),
    # path('risk_assessment/', risk_assessment,
    #      name='risk_assessment'),
    # path('prd_insp_history/', prd_insp_history,
    #      name='prd_insp_history'),
    # path('applicable_overpres_demand_case/',
    #      applicable_overpres_demand_case,
    #      name='applicable_overpres_demand_case'),
    # path('delete_insp_history/<int:pk>/', delete_inspe_history_obj,
    #      name='delete_inspe_history_obj'),
    # path('delete_applic_overpr/<int:pk>/', delete_applic_overpr_obj,
    #      name='delete_applic_overpr_obj'),
]
