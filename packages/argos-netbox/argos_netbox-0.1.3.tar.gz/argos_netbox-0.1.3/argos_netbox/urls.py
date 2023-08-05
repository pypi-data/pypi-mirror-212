from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # LDP
    path('ldp/', views.LDP_ListView.as_view(), name='ldp_list'),
    path('ldp/add/', views.LDP_EditView.as_view(), name='ldp_add'),
    path('ldp/<int:pk>/', views.LDP_View.as_view(), name='ldp'),
    path('ldp/<int:pk>/edit/', views.LDP_EditView.as_view(), name='ldp_edit'),
    path('ldp/<int:pk>/delete/', views.LDP_DeleteView.as_view(), name='ldp_delete'),
    path(
        'ldp/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='ldp_changelog',
        kwargs={'model': models.LDP},
    ),
    # BGP CE
    path('bgp-ce/', views.BGP_CE_ListView.as_view(), name='bgp_ce_list'),
    path('bgp-ce/add/', views.BGP_CE_EditView.as_view(), name='bgp_ce_add'),
    path('bgp-ce/<int:pk>/', views.BGP_CE_View.as_view(), name='bgp_ce'),
    path('bgp-ce/<int:pk>/edit/', views.BGP_CE_EditView.as_view(), name='bgp_ce_edit'),
    path('bgp-ce/<int:pk>/delete/', views.BGP_CE_DeleteView.as_view(), name='bgp_ce_delete'),
    path(
        'bgp-ce/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='bgp_ce_changelog',
        kwargs={'model': models.BGP_CE},
    ),
    # BGP PE
    path('bgp-pe/', views.BGP_PE_ListView.as_view(), name='bgp_pe_list'),
    path('bgp-pe/add/', views.BGP_PE_EditView.as_view(), name='bgp_pe_add'),
    path('bgp-pe/<int:pk>/', views.BGP_PE_View.as_view(), name='bgp_pe'),
    path('bgp-pe/<int:pk>/edit/', views.BGP_PE_EditView.as_view(), name='bgp_pe_edit'),
    path('bgp-pe/<int:pk>/delete/', views.BGP_PE_DeleteView.as_view(), name='bgp_pe_delete'),
    path(
        'bgp-pe/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='bgp_pe_changelog',
        kwargs={'model': models.BGP_PE},
    ),
    # BGP Mesh
    path('bgp-mesh/', views.BGP_Mesh_ListView.as_view(), name='bgp_mesh_list'),
    path('bgp-mesh/add/', views.BGP_Mesh_EditView.as_view(), name='bgp_mesh_add'),
    path('bgp-mesh/<int:pk>/', views.BGP_Mesh_View.as_view(), name='bgp_mesh'),
    path('bgp-mesh/<int:pk>/edit/', views.BGP_Mesh_EditView.as_view(), name='bgp_mesh_edit'),
    path('bgp-mesh/<int:pk>/delete/', views.BGP_Mesh_DeleteView.as_view(), name='bgp_mesh_delete'),
    path(
        'bgp-mesh/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='bgp_mesh_changelog',
        kwargs={'model': models.BGP_Mesh},
    ),
    # Address Family
    path('address-family/', views.Address_Family_ListView.as_view(), name='address_family_list'),
    path('address-family/add/', views.Address_Family_EditView.as_view(), name='address_family_add'),
    path('address-family/<int:pk>/', views.Address_Family_View.as_view(), name='address_family'),
    path('address-family/<int:pk>/edit/', views.Address_Family_EditView.as_view(), name='address_family_edit'),
    path('address-family/<int:pk>/delete/', views.Address_Family_DeleteView.as_view(), name='address_family_delete'),
    path(
        'address-family/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='address_family_changelog',
        kwargs={'model': models.Address_Family},
    ),
    # MPLS Instance
    path('mpls-instance/', views.MPLS_Instance_ListView.as_view(), name='mpls_instance_list'),
    path('mpls-instance/add/', views.MPLS_Instance_EditView.as_view(), name='mpls_instance_add'),
    path('mpls-instance/<int:pk>/', views.MPLS_Instance_View.as_view(), name='mpls_instance'),
    path('mpls-instance/<int:pk>/edit/', views.MPLS_Instance_EditView.as_view(), name='mpls_instance_edit'),
    path('mpls-instance/<int:pk>/delete/', views.MPLS_Instance_DeleteView.as_view(), name='mpls_instance_delete'),
    path(
        'mpls-instance/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='mpls_instance_changelog',
        kwargs={'model': models.MPLS_Instance},
    ),
)
