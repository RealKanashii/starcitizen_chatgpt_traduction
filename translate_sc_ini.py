import openai
from github import Github

# Configuración de OpenAI
openai.api_key = 'TU_API_KEY'

# Configuración de GitHub
g = Github("TU_TOKEN_DE_GITHUB")
repo = g.get_user().get_repo("NOMBRE_DEL_REPO")

def traducir_star_citizen(texto_ingles):
    respuesta = openai.Completion.create(
        engine="gpt-4.0-turbo",
        prompt=f"Traduce el siguiente texto del juego Star Citizen del inglés al castellano, manteniendo el lore o background del juego. Respeta los nombres de los planetas, ubicaciones y personajes, pero traduce todo el resto:\n\nTexto: \"{texto_ingles}\"\n\nTraducción:",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    traduccion = respuesta.choices[0].text.strip()
    return traduccion

def traducir_archivo_github(ruta):
    contenido = repo.get_contents(ruta).decoded_content.decode()
    lineas = contenido.split("\n")
    traducciones = []

    for linea in lineas:
        if "=" in linea:
            var, texto = linea.split("=", 1)
            traducido = traducir_star_citizen(texto.strip())
            traducciones.append(f"{var}={traducido}")
        else:
            traducciones.append(linea)

    traducido_completo = "\n".join(traducciones)
    return traducido_completo

def subir_traduccion_a_github(ruta, contenido_traducido):
    repo.create_file(ruta, "Archivo traducido", contenido_traducido)

ruta_archivo = "ruta/al/archivo_en_github.txt"
contenido_traducido = traducir_archivo_github(ruta_archivo)
ruta_destino = "ruta/al/archivo_traducido_en_github.txt"
subir_traduccion_a_github(ruta_destino, contenido_traducido)
