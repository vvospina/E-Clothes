from datetime import datetime, timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from consejos.mongo import consejos_collection

# 1. AUTENTICACIÓN FIREBASE: 
# El decorador @permission_classes([IsAuthenticated]) obliga a que 
# todas las peticiones a estas funciones incluyan un token válido de 
# Firebase (Bearer Token) en los headers.


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def consejos_list_create(request):
    """
    Vista encargada de:
    - Listar todos los consejos o filtrar por categoría (Método GET).
    - Crear un nuevo consejo ambiental (Método POST).
    Ruta asociada pública base: /api/v1/consejos/
    """
    
    # 2. LISTADO Y FILTRADO POR CATEGORÍA (QUERY PARAMS)

    if request.method == "GET":
        # Captura el parámetro de consulta ?categoria= de la URL (Ej: /api/v1/consejos?categoria=Reutilización)
        categoria = request.GET.get("categoria")
        
        # Construye el filtro para MongoDB: si mandaron categoría busca por ella, si no, trae todo ({})
        query = {"categoria": categoria} if categoria else {}
        
        # Consulta los registros en la base de datos MongoDB
        consejos = list(consejos_collection.find(query))
        
        # Transforma el formato del ID interno de MongoDB (_id) a un string estándar ("id") para el JSON
        for c in consejos:
            c["id"] = str(c.pop("_id"))
            
        # Retorna la lista con código HTTP 200 OK
        return Response(consejos, status=status.HTTP_200_OK)
    
    # 3. CREACIÓN DE UN NUEVO CONSEJO

    elif request.method == "POST":
        # Extrae los datos enviados en el cuerpo (Body) de la petición HTTP
        data = request.data
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        categoria = data.get("categoria")
        
        # Validación de datos obligatorios según el contrato técnico
        if not titulo or not contenido or not categoria:
            # Manejo de códigos HTTP: Retorna 400 Bad Request si faltan datos
            return Response(
                {
                    "code": "INVALID_DATA", 
                    "message": "Faltan atributos obligatorios (titulo, contenido, categoria)"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Estructura el documento listo para insertar con su fecha actual en UTC
        nuevo_consejo = {
            "titulo": titulo,
            "contenido": contenido,
            "categoria": categoria,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Inserta el registro en MongoDB
        result = consejos_collection.insert_one(nuevo_consejo)
        
        # Asigna el ID generado por la base de datos a la respuesta
        nuevo_consejo["id"] = str(result.inserted_id)
        nuevo_consejo.pop("_id", None)
        
        # Manejo de códigos HTTP: Retorna 201 Created al registrar exitosamente
        return Response(nuevo_consejo, status=status.HTTP_201_CREATED)


# 4. CONSULTA POR IDENTIFICADOR ÚNICO (ID)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Exige autenticación con Firebase
def consejo_detail(request, pk):
    """
    Vista encargada de consultar el detalle de un consejo específico.
    Ruta asociada: /api/v1/consejos/{id}/
    """
    try:
        # Convierte el parámetro 'pk' de la URL en un ObjectId válido de MongoDB y realiza la búsqueda
        consejo = consejos_collection.find_one({"_id": ObjectId(pk)})
        
        # Si el documento no existe en la base de datos
        if not consejo:
            # Manejo de códigos HTTP: Retorna 404 Not Found
            return Response(
                {"code": "NOT_FOUND", "message": "Consejo no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Formatea el _id a "id" string para el contrato JSON
        consejo["id"] = str(consejo.pop("_id"))
        
        # Manejo de códigos HTTP: Retorna 200 OK con el recurso encontrado
        return Response(consejo, status=status.HTTP_200_OK)
        
    except Exception:
        # Si el ID proporcionado en la URL no tiene el formato correcto que MongoDB espera
        # Manejo de códigos HTTP: Retorna 400 Bad Request
        return Response(
            {"code": "INVALID_ID", "message": "El formato del ID es inválido"}, 
            status=status.HTTP_400_BAD_REQUEST
        )


# 5. ENDPOINT DE SALUD (HEALTH CHECK)

@api_view(["GET"])
def health(request):
    """
    Endpoint público para verificar el estado del microservicio (usado en Docker / Compose).
    """
    return Response({"status": "ok"}, status=status.HTTP_200_OK)