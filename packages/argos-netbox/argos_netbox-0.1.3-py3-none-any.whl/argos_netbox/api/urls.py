from netbox.api.routers import NetBoxRouter
from . import views


router = NetBoxRouter()
router.register('ldp', views.LDP_ViewSet)
router.register('bgp-ce', views.BGP_CE_ViewSet, basename='bgp_ce')
router.register('bgp-pe', views.BGP_PE_ViewSet, basename='bgp_pe')
router.register('bgp-mesh', views.BGP_Mesh_ViewSet, basename='bgp_mesh')
router.register('address-family', views.Address_Family_ViewSet, basename='address_family')
router.register('mpls-instance', views.MPLS_Instance_ViewSet, basename='mpls_instance')

urlpatterns = router.urls
