from netbox.views import generic
from . import forms, models, tables


#
# Request handlers, response rendering
#


# LDP
class LDP_View(generic.ObjectView):
    queryset = models.LDP.objects.all()


class LDP_ListView(generic.ObjectListView):
    queryset = models.LDP.objects.all()
    table = tables.LDP_Table


class LDP_EditView(generic.ObjectEditView):
    queryset = models.LDP.objects.all()
    form = forms.LDP_Form
    template_name = 'argos_netbox/ldp_edit.html'


class LDP_DeleteView(generic.ObjectDeleteView):
    queryset = models.LDP.objects.all()


# BGP CE
class BGP_CE_View(generic.ObjectView):
    queryset = models.BGP_CE.objects.all()


class BGP_CE_ListView(generic.ObjectListView):
    queryset = models.BGP_CE.objects.all()
    table = tables.BGP_CE_Table


class BGP_CE_EditView(generic.ObjectEditView):
    queryset = models.BGP_CE.objects.all()
    form = forms.BGP_CE_Form


class BGP_CE_DeleteView(generic.ObjectDeleteView):
    queryset = models.BGP_CE.objects.all()


# BGP PE
class BGP_PE_View(generic.ObjectView):
    queryset = models.BGP_PE.objects.all()


class BGP_PE_ListView(generic.ObjectListView):
    queryset = models.BGP_PE.objects.all()
    table = tables.BGP_PE_Table


class BGP_PE_EditView(generic.ObjectEditView):
    queryset = models.BGP_PE.objects.all()
    form = forms.BGP_PE_Form


class BGP_PE_DeleteView(generic.ObjectDeleteView):
    queryset = models.BGP_PE.objects.all()


# BGP Mesh
class BGP_Mesh_View(generic.ObjectView):
    queryset = models.BGP_Mesh.objects.all()


class BGP_Mesh_ListView(generic.ObjectListView):
    queryset = models.BGP_Mesh.objects.all()
    table = tables.BGP_Mesh_Table


class BGP_Mesh_EditView(generic.ObjectEditView):
    queryset = models.BGP_Mesh.objects.all()
    form = forms.BGP_Mesh_Form


class BGP_Mesh_DeleteView(generic.ObjectDeleteView):
    queryset = models.BGP_Mesh.objects.all()


# Address Family
class Address_Family_View(generic.ObjectView):
    queryset = models.Address_Family.objects.all()


class Address_Family_ListView(generic.ObjectListView):
    queryset = models.Address_Family.objects.all()
    table = tables.Address_Family_Table


class Address_Family_EditView(generic.ObjectEditView):
    queryset = models.Address_Family.objects.all()
    form = forms.Address_Family_Form
    template_name = 'argos_netbox/address_family_edit.html'


class Address_Family_DeleteView(generic.ObjectDeleteView):
    queryset = models.Address_Family.objects.all()


# MPLS Instance
class MPLS_Instance_View(generic.ObjectView):
    queryset = models.MPLS_Instance.objects.all()


class MPLS_Instance_ListView(generic.ObjectListView):
    queryset = models.MPLS_Instance.objects.all()
    table = tables.MPLS_Instance_Table


class MPLS_Instance_EditView(generic.ObjectEditView):
    queryset = models.MPLS_Instance.objects.all()
    form = forms.MPLS_Instance_Form


class MPLS_Instance_DeleteView(generic.ObjectDeleteView):
    queryset = models.MPLS_Instance.objects.all()
