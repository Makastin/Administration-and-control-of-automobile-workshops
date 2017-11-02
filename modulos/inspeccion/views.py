# encoding: utf-8

from base64 import b64decode

from django import http
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.http import QueryDict
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.template import RequestContext
from django.conf import settings
from weasyprint import HTML, CSS

from core.views import BaseWebMixin
from modulos.macros.models import ConsecutivoInspeccion, Macros
from modulos.vehiculo.models import Modelo, Vehiculo
from modulos.propietario.models import Propietario,PropietarioVehiculo,Licencia

from .forms import DatosBasicosForm, CargaDocumentosForm, CargaImprontaForm
from .forms import CargaAnalisisForm, FotografiasVehiculoForm
from .models import Inspeccion, InspeccionDetalle, InspeccionFotografia, InspeccionImpronta


class DatosBasicosView(BaseWebMixin):

    def get(self, request, *args, **kwargs):
        ci = ConsecutivoInspeccion.objects.last()

        if hasattr(ci, 'codigo_inspeccion'):
            ci = ci.codigo_inspeccion + 1

        form = DatosBasicosForm
        context = {'ci': ci, 'form': form}
        return render(request, 'inspeccion/datos-basicos.html', context)

    def post(self, request, *args, **kwargs):
        ci = ConsecutivoInspeccion.objects.last()
        if hasattr(ci, 'codigo_inspeccion'):
            ci = ci.codigo_inspeccion + 1

        form = DatosBasicosForm(request.POST)
        if form.is_valid():
            placa = form.cleaned_data['placa'] #redy
            placa_2 = form.cleaned_data['placa_2'] #redy
            numero_rombo = form.cleaned_data['numero_rombo'] #redy
            ciudad = form.cleaned_data['ciudad'] #redy


            #tipo_propietario
            tipo_propietario = form.cleaned_data['tipo_propietario'] #redy

            #Propietario Empresarial
            razon_social = form.cleaned_data['razon_social'] #redy
            nit = form.cleaned_data['nit'] #redy
            nit_2 = form.cleaned_data['nit_2'] #redy

            #Propietario Personal
            nombres = form.cleaned_data['nombres'] #redy
            apellidos = form.cleaned_data['apellidos'] #redy
            tipo_identificacion = form.cleaned_data['tipo_identificacion'] #redy
            cedula_ciudadania = form.cleaned_data['cedula_ciudadania'] #redy
            edad = form.cleaned_data['edad'] #redy
            profesion_propietario= form.cleaned_data['profesion_propietario'] #redy

            #Datos para ambos tipos de propietario
            direccion = form.cleaned_data['direccion'] #redy
            telefono_fijo = form.cleaned_data['telefono_fijo'] #redy
            telefono_celular = form.cleaned_data['telefono_celular'] #redy
            ciudad_2 = form.cleaned_data['ciudad_2'] #redy

            #Datos Basico del Vehiculo
            marca_vehiculo = form.cleaned_data['marca_vehiculo'] #redy
            clase_vehiculo = form.cleaned_data['clase_vehiculo'] #redy
            tipo_vehiculo = form.cleaned_data['tipo_vehiculo'] #redy
            modelo_vehiculo = form.cleaned_data['modelo_vehiculo'] #redy
            carroceria_vehiculo = form.cleaned_data['carroceria_vehiculo'] #redy
            tipo_caja = form.cleaned_data['tipo_caja'] #redy
            nacionalidad_vehiculo = form.cleaned_data['nacionalidad_vehiculo'] #redy
            color_vehiculo = form.cleaned_data['color_vehiculo'] #redy
            tipo_pintura = form.cleaned_data['tipo_pintura'] #redy
            tipo_combustible = form.cleaned_data['tipo_combustible']
            cilindraje_vehiculo = form.cleaned_data['cilindraje_vehiculo']
            numero_motor_vehiculo = form.cleaned_data['numero_motor_vehiculo'] #redy
            numero_serie_vehiculo = form.cleaned_data['numero_serie_vehiculo'] #redy
            numero_chasis_vehiculo = form.cleaned_data['numero_chasis_vehiculo'] #redy
            servicio_vehiculo = form.cleaned_data['servicio_vehiculo'] #redy
            kilometraje_vehiculo = form.cleaned_data['kilometraje_vehiculo'] #redy

            #Valores
            v_r_cliente = form.cleaned_data['v_r_cliente'] #redy
            v_r_empresa = form.cleaned_data['v_r_empresa'] #redy
            v_r_fasecolda = form.cleaned_data['v_r_fasecolda'] #redy
            v_r_accesorios = form.cleaned_data['v_r_accesorios'] #redy


            if placa != placa_2:
                context = {'ci': ci, 'form': form}
                messages.warning(request, u'Las placas no coinciden.')
                return render(request, 'inspeccion/datos-basicos.html', context)

            #Insertamos un nuevo Propietario.
            tipos_propietarios = {1:"empresarial",2:"personal",}
            tipo_propietario = tipos_propietarios.get(int(tipo_propietario),'no_seleccionado')

            if tipo_propietario == "empresarial":
                if nit == nit_2:
                    #Buscar NIT y validar si existe y si existe retornar el form con un mensaje
                    nuevo_propietario = Propietario.objects.create(
                        tipo_propietario = tipo_propietario,
                        numero_documento = nit,
                        nombre = razon_social,
                        telefono_fijo = telefono_fijo,
                        telefono_celular = telefono_celular,
                        direccion = direccion,
                        ciudad_id = ciudad_2.id,
                    )
                else:
                    context = {'ci': ci, 'form': form}
                    messages.warning(request, u'Los codigos NIT no coinciden.')
                    return render(request, 'inspeccion/datos-basicos.html', context)
                    #Retornamos un error en el formulario ya que los nit no son iguales.
            elif tipo_propietario == "personal" :
                #Se puede buscar el propietario antes si existe se avisa que ya esta registrado.
                nuevo_propietario = Propietario.objects.create(
                    tipo_propietario = tipo_propietario,
                    tipo_documento = tipo_identificacion,
                    numero_documento = cedula_ciudadania,
                    nombre = nombres,
                    apellido = apellidos,
                    edad = edad,
                    telefono_fijo = telefono_fijo,
                    telefono_celular = telefono_celular,
                    direccion = direccion,
                    profesion = profesion_propietario,
                    ciudad_id = ciudad_2.id,
                )
            else:
                messages.warning(request, u'Tipo de Propietario no seleccionado')
                context = {'ci': ci, 'form': form}
                return render(request, 'inspeccion/datos-basicos.html', context)

            #Insertamos el Modelo
            modelo, creado= Modelo.objects.get_or_create(
                nombre__icontains=modelo_vehiculo,
                marca_id = marca_vehiculo.id,
                defaults={'marca_id' : marca_vehiculo.id,'nombre' : modelo_vehiculo}
            )

            #Insertamos un nuevo vehiculo.
            nuevo_vehiculo = Vehiculo.objects.create(
                modelo_id = modelo.id,
                ano = 1999, #No existe en el form
                clase = clase_vehiculo,
                tipo = tipo_vehiculo,
                carroceria = carroceria_vehiculo,
                tipo_caja = tipo_caja,
                tipo_combustible = tipo_combustible,
                cilindraje = cilindraje_vehiculo,
                nacionalidad = nacionalidad_vehiculo,
            )

            #Proseguimos con la carga de informacion sea el tipo de propietario.
            vinculacion_propietario_vehiculo = PropietarioVehiculo.objects.create(
                propietario_id = nuevo_propietario.id,
                vehiculo_id = nuevo_vehiculo.id,
                color = color_vehiculo,
                tipo_pintura = tipo_pintura,
                numero_serie = numero_serie_vehiculo,
                numero_chasis = numero_chasis_vehiculo,
                numero_motor =  numero_motor_vehiculo,
                placa = placa,
                ciudad_id = ciudad.id,
                rombo =  numero_rombo,
            )

            #Insertamos inspeccion
            nueva_inspeccion = Inspeccion.objects.create(
                propietario_vehiculo_id = vinculacion_propietario_vehiculo.id,
                tipo_servicio = servicio_vehiculo,
                kilometraje = kilometraje_vehiculo,
                numero_inspeccion = ci,
                paso = 'carga_documentos',
                v_r_cliente = v_r_cliente,
                v_r_empresa = v_r_empresa,
                v_r_fasecolda = v_r_fasecolda,
                v_r_accesorios =v_r_accesorios,
            )
            ConsecutivoInspeccion.objects.create(
                codigo_inspeccion = ci,
            )

            print "===========DEBUG========="
            print "Nuevo Vehiculo Agregado el ID es: " + str(nuevo_vehiculo.id)
            print "El tipo de propietario es: " + tipo_propietario
            print "Nuevo Propietario Agregado el ID es: " + str(nuevo_propietario.id)
            print "Vinculacion Propietario-Vehiculo el ID es: " + str(vinculacion_propietario_vehiculo.id)
            print "Nueva Inspeccion Agregada el ID es:" + str(nueva_inspeccion.id)

            if 'carga_documentos' in request.session['user_perms'] or request.user.is_superuser:
                return redirect(reverse('inspeccion:carga_documentos', args=(nueva_inspeccion.id,)))
            else:
                messages.success(request, u'Datos basicos agregados')
                form = DatosBasicosForm
                context = {'ci': ci, 'form': form}
                return render(request, 'inspeccion/datos-basicos.html', context)
        else:
            messages.warning(request, u'Formulario no Valido')
            context = {'ci': ci, 'form': form}
            return render(request, 'inspeccion/datos-basicos.html', context)

class CargaDocumentosView(BaseWebMixin):
    def get(self, request, *args, **kwargs):
        form = CargaDocumentosForm
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        propietario_vehiculo = PropietarioVehiculo.objects.get(id=inspeccion.propietario_vehiculo_id)
        licencia_propietario = Licencia.objects.filter(propietario_id = propietario_vehiculo.propietario_id).values()

        if licencia_propietario.exists():
            imagen_delantera = licencia_propietario[0]["imagen_delantera"]
            imagen_trasera = licencia_propietario[0]["imagen_trasera"]
        else:
            imagen_delantera = ""
            imagen_trasera = ""

        context = {
            'inspeccion': inspeccion,
            'form':form,
            'imagen_delantera':imagen_delantera,
            'imagen_trasera':imagen_trasera
            }

        return render(request, 'inspeccion/carga-de-documentos.html', context)

    def post(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        form = CargaDocumentosForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            licencia_propietario, created = Licencia.objects.update_or_create(
                propietario = inspeccion.propietario_vehiculo.propietario,
                defaults = {
                    'imagen_delantera': data['fotografia_delantera'],
                    'imagen_trasera': data['fotografia_trasera'],
                })

            inspeccion.paso = 'inspeccion_visual'
            inspeccion.save()

            if 'inspeccion_visual' in request.session['user_perms'] or request.user.is_superuser:
                return redirect(reverse('inspeccion:inspeccion_visual', args=(kwargs.get('pk'))))
            else:
                messages.success(request, u'Licencia de transito agregada')
                licencia_propietario = Licencia.objects.filter(propietario_id = licencia_propietario.propietario_id).values()
                imagen_delantera = licencia_propietario[0]["imagen_delantera"]
                imagen_trasera = licencia_propietario[0]["imagen_trasera"]
                context = {
                    'form': form,
                    'imagen_delantera': imagen_delantera,
                    'imagen_trasera': imagen_trasera,
                }
                return render(request, 'inspeccion/carga-de-documentos.html', context)

        messages.warning(request,u'Formulario no valido')
        return render(request, 'inspeccion/carga-de-documentos.html')


class InspeccionVisualView(BaseWebMixin):
    def get(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        step = request.GET.get('step', 'motor')
        context = {}
        ins_detalle = inspeccion.inspecciondetalle_set.filter(macro_value__tipo=step).first()

        if ins_detalle:
            context['inspeccion_detalle'] = ins_detalle

        template = {
            'motor': 'inspeccion/inspeccion-visual-1.html',
            'exterior': 'inspeccion/inspeccion-visual-2.html',
            'interior': 'inspeccion/inspeccion-visual-3.html',
            'parte_baja': 'inspeccion/inspeccion-visual-4.html'
        }.get(step, 'motor')

        macros = Macros.objects.all()

        _macros = {
            'motor': macros.filter(tipo=step),
            'exterior': macros.filter(tipo=step),
            'interior': macros.filter(tipo=step),
            'parte_baja': macros.filter(tipo=step)
        }.get(step, 'motor')

        context['macros'] = _macros
        context['inspeccion'] = inspeccion

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        step = request.GET.get('step', 'motor')
        macros = get_list_or_404(Macros, tipo=step)
        data = request.POST
        macro_values = {'tipo': request.GET.get('step', 'motor'), 'values': []}

        for macro in macros:
            macro_values['values'].append({'nombre': macro.nombre, 'slug': macro.nombre_slug, 'condicion': data.get(macro.nombre_slug, 'no_aplica')})

        inspeccion_detalle, created = InspeccionDetalle.objects.update_or_create(
                inspeccion = inspeccion,
                macro_value__tipo = step,
                defaults = {
                    'observacion': data.get('observacion'),
                    'macro_value' :macro_values
                })

        if step == 'parte_baja':
            inspeccion.paso = 'fotografias_vehiculo'
            inspeccion.save()

            if 'fotografias_vehiculo' in request.session['user_perms'] or request.user.is_superuser:
                return redirect(reverse('inspeccion:fotografias_vehiculo', args=(kwargs.get('pk'))))

            messages.success(request, u'Inspeccion Visual agregada')
            return redirect(reverse('inspeccion:listar'))

        return redirect(self.next_step(step))

    def next_step(self, actual):
        return {
            'motor': '%s?%s' % (reverse('inspeccion:inspeccion_visual', args=(self.kwargs.get('pk'))), QueryDict('step=exterior').urlencode()),
            'exterior': '%s?%s' % (reverse('inspeccion:inspeccion_visual', args=(self.kwargs.get('pk'))), QueryDict('step=interior').urlencode()),
            'interior': '%s?%s' % (reverse('inspeccion:inspeccion_visual', args=(self.kwargs.get('pk'))), QueryDict('step=parte_baja').urlencode()),
        }.get(actual, reverse('inspeccion:listar'))


class FotografiasVehiculoView(BaseWebMixin):
    def get(self, request, *args, **kwargs):

        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        inspeccion_fotografia = InspeccionFotografia.objects.filter(inspeccion_id=kwargs.get('pk')).values()
        form = FotografiasVehiculoForm
        context = {'form': form, 'inspeccion': inspeccion}

        if inspeccion_fotografia.exists():
            context['inspeccion_fotografia'] = inspeccion_fotografia[0]
        return render(request, 'inspeccion/fotografias-vehiculo.html', context)

    def post(self, request, *args, **kwargs):

        inspeccion_id = kwargs.get('pk');
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=inspeccion_id)

        form = FotografiasVehiculoForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            raw_data_fotografia_superior_derecha =  data['fotografia_superior_derecha']
            raw_data_fotografia_superior_izquierda =  data['fotografia_superior_izquierda']
            raw_data_fotografia_delantera =  data['fotografia_delantera']
            raw_data_fotografia_trasera =  data['fotografia_trasera']
            raw_data_fotografia_interior =  data['fotografia_interior']

            image_data_superior_derecha = b64decode(raw_data_fotografia_superior_derecha)
            image_data_superior_izquierda = b64decode(raw_data_fotografia_superior_izquierda)
            image_data_delantera = b64decode(raw_data_fotografia_delantera)
            image_data_trasera = b64decode(raw_data_fotografia_trasera)
            image_data_interior = b64decode(raw_data_fotografia_interior)

            inspeccion_fotografia, creado= InspeccionFotografia.objects.update_or_create(
                inspeccion_id = inspeccion_id,
                defaults={
                    'inspeccion_id' : inspeccion_id,
                    'img_superior_derecha' : ContentFile(image_data_superior_derecha, 'fotografia_superior_derecha_'+str(inspeccion_id)+'.png'),
                    'img_superior_izquierda' : ContentFile(image_data_superior_izquierda, 'fotografia_superior_izquierda_'+str(inspeccion_id)+'.png'),
                    'img_delantera' : ContentFile(image_data_delantera, 'fotografia_delantera_'+str(inspeccion_id)+'.png'),
                    'img_trasera' : ContentFile(image_data_trasera, 'fotografia_trasera_'+str(inspeccion_id)+'.png'),
                    'img_interior' : ContentFile(image_data_interior, 'fotografia_interior_'+str(inspeccion_id)+'.png')
                }
            )

            inspeccion.paso = 'carga_analisis'
            inspeccion.save()

            if 'carga_analisis' in request.session['user_perms'] or request.user.is_superuser:
                return redirect(reverse('inspeccion:carga_analisis', args=(kwargs.get('pk'))))
            else:
                messages.success(request, u'Imagenes agregadas')
                form = FotografiasVehiculoForm
                #Consultamos con el id que nos retorna InspeccionFotografia para obtener
                #las url de las fotos y pasarsela a la interfaz
                context = {'form':form,'inspeccion_fotografia':inspeccion_fotografia, 'inspeccion': inspeccion}
                return render(request, 'inspeccion/fotografias-vehiculo.html', context)

        else:
            messages.warning(request, u'Faltan Imagenes')
            context = {'form': form, 'inspeccion': inspeccion}
            return render(request, 'inspeccion/fotografias-vehiculo.html', context)

        return render(request, 'inspeccion/fotografias-vehiculo.html')


class CargaAnalisisView(BaseWebMixin):
    def get(self, request, *args, **kwargs):

        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        form = CargaAnalisisForm
        context = {'form':form, 'inspeccion': inspeccion}
        return render(request, 'inspeccion/carga-analisis.html', context)

    def post(self, request, *args, **kwargs):

        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        form = CargaAnalisisForm(request.POST,request.FILES)
        context = {'form':form, 'inspeccion': inspeccion}

        if form.is_valid():
            data = form.cleaned_data
            analisis = data['analisis']
            for linea in analisis:
                if "10050" in linea:
                    print linea
            if 'cargar_improntas' in request.session['user_perms'] or request.user.is_superuser:
                return redirect(reverse('inspeccion:cargar_improntas', args=(kwargs.get('pk'))))
        return render(request, 'inspeccion/carga-analisis.html',context)


class CargarImprontasView(BaseWebMixin):
    def get(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        form = CargaImprontaForm
        context = {'form':form, 'inspeccion': inspeccion}
        return render(request, 'inspeccion/carga-improntas.html',context)
    
    def post(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, finalizado=False, id=kwargs.get('pk'))
        form = CargaImprontaForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            impronta = data['impronta']
            inspeccion_impronta, creado= InspeccionImpronta.objects.update_or_create(
                inspeccion_id = kwargs.get('pk'),
                defaults={
                    'inspeccion_id' : kwargs.get('pk'),
                    'impronta' : impronta
                }
            )
            inspeccion.finalizado = True
            inspeccion.save()
            return redirect(reverse('inicio'))
        context = {'form':form, 'inspeccion': inspeccion}
        return render(request, 'inspeccion/carga-improntas.html', context)


class InspeccionListView(BaseWebMixin):
    def get(self, request, *args, **kwargs):
        placa = request.GET.get('placa', False)
        inspecciones = Inspeccion.objects.all().order_by('-id')

        if placa:
            inspecciones = inspecciones.filter(propietario_vehiculo__placa__icontains=placa)

        paginator = Paginator(inspecciones, 10)
        page = request.GET.get('page')
        try:
            inspecciones = paginator.page(page)
        except PageNotAnInteger:
            inspecciones = paginator.page(1)
        except EmptyPage:
            inspecciones = paginator.page(paginator.num_pages)
        return render(request, 'inspeccion/listar.html', {'inspecciones': inspecciones})


class InspeccionReporteView(BaseWebMixin):
    def get(self, request, *args, **kwargs):
        inspeccion = get_object_or_404(Inspeccion, id=kwargs.get('pk'))
        context = {
            'inspeccion': inspeccion,
            'macro_motor': inspeccion.inspecciondetalle_set.filter(macro_value__tipo='motor').first(),
            'macro_exterior': inspeccion.inspecciondetalle_set.filter(macro_value__tipo='exterior').first(),
            'macro_interior': inspeccion.inspecciondetalle_set.filter(macro_value__tipo='interior').first(),
            'macro_partebaja': inspeccion.inspecciondetalle_set.filter(macro_value__tipo='parte_baja').first(),
            'fotografia': inspeccion.inspeccionfotografia_set.first()
            }

        html_template = get_template('inspeccion/plantilla-reporte.html')
        rendered_html = html_template.render(RequestContext(request, context)).encode(encoding="UTF-8")

        pdf_file = HTML(string=rendered_html, base_url=request.build_absolute_uri()).write_pdf()

        response = http.HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="inspeccion.pdf"'

        return response
