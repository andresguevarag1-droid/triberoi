#!/usr/bin/env python3
"""Genera las páginas del sitio de TRIBEROI.

Cada página toma el contenido de <main> de su archivo actual y lo envuelve con
el encabezado, pie, metadatos SEO y datos estructurados comunes. Así los cambios
globales (contacto, schema, íconos) se hacen en un solo lugar.

Uso: python3 tools/build.py   (desde la raíz del repo)
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.triberoi.net"
UPDATED = "2026-10-25"

ORG = {
    "name": "TRIBEROI Technology",
    "legal": "TRIBEROI, S.A.",
    "tel": "+50230608643",
    "tel_h": "+502 3060 8643",
    "email": "info@triberoi.net",
    "wa": "https://wa.me/50230608643",
    "street": "25 avenida 1-89, zona 15",
    "postal": "01015",
    "city": "Ciudad de Guatemala",
    "maps": "https://www.google.com/maps/search/?api=1&query=25+avenida+1-89+zona+15+Ciudad+de+Guatemala",
    "maps_h": "https://www.google.com/maps/search/?api=1&amp;query=25+avenida+1-89+zona+15+Ciudad+de+Guatemala",
}

SERVICES = [
    ("software", "Software a la medida", "Sistemas hechos para los procesos de cada empresa, desde herramientas internas hasta plataformas de gestión."),
    ("web", "Aplicaciones y sitios web", "Sitios corporativos, portales para clientes y aplicaciones web responsivas y fáciles de actualizar."),
    ("hosting", "Hosting y nube", "Alojamiento de sitios y sistemas en infraestructura confiable, con respaldos automáticos y monitoreo."),
    ("soporte", "Soporte y mantenimiento", "Soporte técnico, actualizaciones de seguridad, corrección de errores y mejoras continuas."),
    ("datos", "Bases de datos", "Diseño, migración, optimización y respaldo de bases de datos empresariales."),
    ("marketing", "Marketing digital", "Estrategia digital, campañas en redes sociales y buscadores, medición y contenido."),
    ("talento", "Outsourcing de talento TI", "Reclutamiento, contratación, capacitación y administración de profesionales de TI."),
    ("consultoria", "Consultoría tecnológica", "Diagnóstico tecnológico, hoja de ruta y acompañamiento en la selección e implementación de herramientas."),
]

HOME_FAQ = [
    ("¿Qué hace TRIBEROI?", "TRIBEROI es una empresa de tecnología con sede en la Ciudad de Guatemala. Desarrollamos software a la medida y aplicaciones web, ofrecemos hosting, soporte y administración de bases de datos, y apoyamos con marketing digital, outsourcing de talento TI y consultoría tecnológica."),
    ("¿Dónde están ubicados?", "Nuestra oficina está en la 25 avenida 1-89, zona 15, Ciudad de Guatemala. Atendemos de forma presencial y remota, así que también trabajamos con empresas de otros departamentos."),
    ("¿Cuánto cuesta un software o un sitio web?", "Depende de lo que necesites. Después de una primera conversación te enviamos una propuesta por escrito con alcance, tiempos y costo, antes de empezar cualquier trabajo."),
    ("¿Cuánto tiempo toma un proyecto?", "Depende del alcance. Un sitio corporativo suele tomar semanas y un sistema a la medida puede tomar varios meses. En la propuesta te damos un calendario por etapas para que sepas qué recibes y cuándo."),
    ("¿Dan soporte después de entregar el proyecto?", "Sí. Ofrecemos soporte técnico, actualizaciones de seguridad, corrección de errores y mejoras continuas después del lanzamiento."),
    ("¿Pueden aportar personal de TI a mi empresa?", "Sí. Reclutamos, capacitamos y administramos profesionales de tecnología que se integran a tu equipo, por proyecto o de forma continua."),
]

SVC_FAQ = [
    ("¿Puedo contratar un solo servicio?", "Sí. Puedes contratar un servicio puntual, como un sitio web o soporte, o combinar varios. En ambos casos trabajas con el mismo equipo."),
    ("¿El software queda a nombre de mi empresa?", "Sí. Lo que desarrollamos para ti se entrega con su código y documentación, y los accesos a dominios, servidores y cuentas quedan a nombre de tu empresa."),
    ("¿Trabajan con sistemas que ya tenemos?", "Sí. Podemos mejorar, integrar o migrar sistemas existentes. Primero revisamos lo que tienes y te decimos qué conviene conservar y qué conviene cambiar."),
    ("¿Cómo funciona el soporte?", "Nos escribes por correo o WhatsApp y te responde una persona del equipo que ya conoce tu sistema. El nivel de soporte se acuerda por escrito en la propuesta."),
]

PAGES = {
    "index.html": dict(path="/", nav="/", kind="WebPage",
        title="TRIBEROI | Desarrollo de software y servicios TI en Guatemala",
        desc="TRIBEROI es una empresa de tecnología en la Ciudad de Guatemala: software a la medida, aplicaciones y sitios web, hosting, soporte, bases de datos, marketing digital y talento TI."),
    "servicios/index.html": dict(path="/servicios", nav="/servicios", kind="CollectionPage", crumb="Servicios",
        title="Servicios de software, web y TI en Guatemala | TRIBEROI",
        desc="Software a la medida, aplicaciones y sitios web, hosting y nube, soporte, bases de datos, marketing digital, outsourcing de talento TI y consultoría tecnológica en Guatemala."),
    "nosotros/index.html": dict(path="/nosotros", nav="/nosotros", kind="AboutPage", crumb="Nosotros",
        title="Nosotros | TRIBEROI, empresa guatemalteca de tecnología",
        desc="TRIBEROI, S.A. es una empresa de tecnología con sede en la zona 15 de la Ciudad de Guatemala. Conoce nuestra misión, visión y forma de trabajo."),
    "contacto/index.html": dict(path="/contacto", nav="/contacto", kind="ContactPage", crumb="Contacto",
        title="Contacto | TRIBEROI Technology, Guatemala",
        desc="Escríbenos a info@triberoi.net o al +502 3060 8643. Oficina en 25 avenida 1-89, zona 15, Ciudad de Guatemala. Te responde una persona del equipo."),
    "privacidad/index.html": dict(path="/privacidad", nav=None, kind="WebPage", crumb="Aviso de privacidad",
        title="Aviso de privacidad | TRIBEROI",
        desc="Cómo TRIBEROI, S.A. trata los datos que compartes al escribirnos por el sitio web, correo o WhatsApp."),
    "404.html": dict(path="/404", nav=None, kind=None, noindex=True,
        title="Página no encontrada | TRIBEROI",
        desc="La página que buscas no existe o cambió de dirección."),
}

ICON_WA = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.6-5.4A8.5 8.5 0 1 1 21 11.5z"/></svg>'


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n</script>"


def org_node():
    return {
        "@type": ["Organization", "ProfessionalService"],
        "@id": SITE + "/#organizacion",
        "name": ORG["name"], "alternateName": "TRIBEROI", "legalName": ORG["legal"],
        "url": SITE + "/",
        "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png", "width": 600, "height": 242},
        "image": SITE + "/assets/og-triberoi.png",
        "slogan": "Hacemos que la tecnología trabaje para tu empresa.",
        "description": "Empresa guatemalteca de tecnología: desarrollo de software a la medida, aplicaciones y sitios web, hosting, soporte, bases de datos, marketing digital, outsourcing de talento TI y consultoría tecnológica.",
        "foundingDate": "2026-04-28",
        "foundingLocation": {"@type": "Place", "name": "Ciudad de Guatemala, Guatemala"},
        "telephone": ORG["tel"], "email": ORG["email"],
        "address": {"@type": "PostalAddress", "streetAddress": ORG["street"], "postalCode": ORG["postal"],
                    "addressLocality": ORG["city"], "addressRegion": "Guatemala", "addressCountry": "GT"},
        "hasMap": ORG["maps"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}],
        "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": ORG["tel"],
                          "email": ORG["email"], "areaServed": "GT", "availableLanguage": ["es"]}],
        "areaServed": {"@type": "Country", "name": "Guatemala"},
        "knowsAbout": ["Desarrollo de software", "Desarrollo web", "Hosting", "Computación en la nube",
                        "Bases de datos", "Soporte técnico", "Marketing digital", "Outsourcing de TI", "Consultoría tecnológica"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@id": f"{SITE}/servicios#{sid}"}} for sid, _, _ in SERVICES],
    }


def service_nodes():
    return [{"@type": "Service", "@id": f"{SITE}/servicios#{sid}", "name": name, "description": d,
             "serviceType": name, "url": f"{SITE}/servicios#{sid}",
             "provider": {"@id": SITE + "/#organizacion"}, "areaServed": {"@type": "Country", "name": "Guatemala"}}
            for sid, name, d in SERVICES]


def faq_node(items, page_url):
    return {"@type": "FAQPage", "@id": page_url + "#preguntas", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def faq_html(items, first_open=True):
    out = []
    for i, (q, a) in enumerate(items):
        op = " open" if (i == 0 and first_open) else ""
        out.append(f'<details{op}><summary>{q}<span class="pm" aria-hidden="true"></span></summary><p>{a}</p></details>')
    return '<div class="faq-list">' + "".join(out) + "</div>"


def schema(key, p):
    url = SITE + (p["path"] if p["path"] != "/" else "/")
    graph = [org_node(), {"@type": "WebSite", "@id": SITE + "/#sitio", "url": SITE + "/", "name": ORG["name"],
                          "inLanguage": "es-GT", "publisher": {"@id": SITE + "/#organizacion"}}]
    page = {"@type": p["kind"], "@id": url + "#pagina", "url": url, "name": p["title"], "description": p["desc"],
            "inLanguage": "es-GT", "isPartOf": {"@id": SITE + "/#sitio"}, "about": {"@id": SITE + "/#organizacion"},
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/og-triberoi.png"},
            "dateModified": UPDATED}
    if p.get("crumb"):
        page["breadcrumb"] = {"@id": url + "#migas"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#migas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]})
    graph.append(page)
    if key in ("index.html", "servicios/index.html"):
        graph += service_nodes()
    if key == "index.html":
        graph.append(faq_node(HOME_FAQ, url))
    if key == "servicios/index.html":
        graph.append(faq_node(SVC_FAQ, url))
    return ld({"@context": "https://schema.org", "@graph": graph})


def head(key, p):
    url = SITE + p["path"] if p["path"] != "/" else SITE + "/"
    robots = "noindex, follow" if p.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    canon = "" if p.get("noindex") else (
        f'<link rel="canonical" href="{url}">\n'
        f'<link rel="alternate" hreflang="es-GT" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">\n')
    preload_img = ""
    if key == "index.html":
        preload_img = ('<link rel="preload" as="image" href="' + img_url(HERO_ID, 960, 25, 22) + '" imagesrcset="'
                       + srcset(HERO_ID, 25, 22) + '" imagesizes="(max-width: 900px) 100vw, 46vw" fetchpriority="high">\n')
    og = "" if p.get("noindex") else f"""<meta property="og:type" content="website"><meta property="og:locale" content="es_GT"><meta property="og:site_name" content="{ORG['name']}">
<meta property="og:title" content="{p['title']}"><meta property="og:description" content="{p['desc']}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-triberoi.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="TRIBEROI: Hacemos que la tecnología trabaje para tu empresa">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{p['title']}"><meta name="twitter:description" content="{p['desc']}"><meta name="twitter:image" content="{SITE}/assets/og-triberoi.png">
"""
    sch = schema(key, p) if p.get("kind") else ""
    return f"""<!doctype html>
<html lang="es-GT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
{canon}<meta name="robots" content="{robots}">
<meta name="author" content="{ORG['legal']}">
<meta name="geo.region" content="GT-GU"><meta name="geo.placename" content="Ciudad de Guatemala">
{og}<meta name="theme-color" content="#F6F7F4">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/simbolo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/poppins-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com" crossorigin>
{preload_img}<link rel="stylesheet" href="/assets/styles.css?v=5">
{sch}
</head>"""


def header(p):
    links = [("/", "Inicio"), ("/servicios", "Servicios"), ("/nosotros", "Nosotros"), ("/contacto", "Contacto")]
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if p.get("nav") == h else ""}>{t}</a>' for h, t in links)
    return f"""<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="TRIBEROI, ir al inicio"><img src="/assets/logo.svg" alt="TRIBEROI Technology" width="101" height="38"></a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="7" x2="21" y2="7"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="17" x2="21" y2="17"/></svg></button>
    <nav class="nav" id="nav" aria-label="Principal">
      {nav}
      <a class="btn btn-ink" href="/contacto">Agendar una llamada</a>
    </nav>
  </div>
</header>"""


FOOTER = f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div><p class="foot-brand"><img src="/assets/simbolo.svg" alt="" width="40" height="35"><span>TRIBEROI</span></p><p>Empresa de desarrollo de software y servicios TI en la Ciudad de Guatemala.</p></div>
      <div><h2>Sitio</h2><ul><li><a href="/">Inicio</a></li><li><a href="/servicios">Servicios</a></li><li><a href="/nosotros">Nosotros</a></li><li><a href="/contacto">Contacto</a></li></ul></div>
      <div><h2>Servicios</h2><ul><li><a href="/servicios#software">Software a la medida</a></li><li><a href="/servicios#web">Aplicaciones web</a></li><li><a href="/servicios#soporte">Soporte</a></li><li><a href="/servicios#talento">Talento TI</a></li></ul></div>
      <div><h2>Contacto</h2><address><ul><li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li><li><a href="tel:{ORG['tel']}">{ORG['tel_h']}</a></li><li><a href="{ORG['wa']}" target="_blank" rel="noopener">Escríbenos por WhatsApp</a></li><li><a href="{ORG['maps_h']}" target="_blank" rel="noopener">{ORG['street']}<br>{ORG['city']} {ORG['postal']}</a></li></ul></address></div>
    </div>
    <div class="legal"><span>© 2026 {ORG['legal']} Todos los derechos reservados.</span><a href="/privacidad">Aviso de privacidad</a></div>
  </div>
</footer>
<a class="wa-float" href="{ORG['wa']}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp al {ORG['tel_h']}">{ICON_WA}<span>WhatsApp</span></a>
<script src="/assets/app.js?v=5" defer></script>
</body>
</html>
"""

# ---------- Fotos (CDN de Unsplash, recortadas al tamaño exacto del contenedor) ----------
HERO_ID = "photo-1758691737568-a1572060ce5a"
PEOPLE_ID = "photo-1676277758484-908057468cca"
ABOUT_ID = "photo-1758519288969-4806f015852d"


def img_url(pid, w, rw, rh):
    h = round(w * rh / rw)
    return f"https://images.unsplash.com/{pid}?auto=format&amp;fit=crop&amp;crop=faces,center&amp;w={w}&amp;h={h}&amp;q=72"


def srcset(pid, rw, rh):
    return ", ".join(f"{img_url(pid, w, rw, rh)} {w}w" for w in (480, 720, 960, 1280))


def picture(pid, rw, rh, alt, eager=False):
    attrs = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{img_url(pid, 960, rw, rh)}" srcset="{srcset(pid, rw, rh)}" '
            f'sizes="(max-width: 900px) calc(100vw - 32px), 46vw" alt="{alt}" width="960" height="{round(960*rh/rw)}" {attrs}>')


def get_main(path):
    s = (ROOT / path).read_text()
    m = re.search(r"<main id=\"contenido\">(.*)</main>", s, re.S)
    return m.group(1) if m else None


PRIV_CHECK_LABEL = '<span>Acepto el <a href="/privacidad">aviso de privacidad</a> y que TRIBEROI use estos datos para responder mi mensaje.</span>'


def transform(key, main):
    main = re.sub(r'<img src="https://unsplash\.com/photos/YyJNda7nsPo[^>]*>',
                  picture(HERO_ID, 25, 22, "Equipo de trabajo conversando alrededor de una mesa en una oficina", eager=True), main)
    main = re.sub(r'<img src="https://unsplash\.com/photos/s8PUvwNMqfw[^>]*>',
                  picture(PEOPLE_ID, 40, 33, "Personas trabajando juntas con sus laptops en una mesa"), main)
    main = re.sub(r'<img src="https://unsplash\.com/photos/pMFXOmP5Z1M[^>]*>',
                  picture(ABOUT_ID, 5, 4, "Dos personas revisando juntas un proyecto en una laptop"), main)
    if key == "index.html":
        main = re.sub(r'<div class="faq-list">.*?</div>\n', faq_html(HOME_FAQ) + "\n", main, flags=re.S)
        main = main.replace('<section>\n  <div class="wrap faq">', '<section id="preguntas">\n  <div class="wrap faq">')
        if 'id="h-priv"' not in main:
            main = main.replace('      <button class="btn btn-ink" type="submit">Enviar mensaje</button>',
                '      <label class="check" for="h-priv"><input id="h-priv" name="privacidad" type="checkbox" required>' + PRIV_CHECK_LABEL + '</label>\n'
                '      <button class="btn btn-ink" type="submit">Enviar mensaje</button>')
        main = re.sub(r'\n\s*\n(\s*<div class="field full"><label for="h-servicio">)', r'\n\1', main)
        main = re.sub(r'(</textarea></div>)\n\s*\n', r'\1\n', main)
    if key == "contacto/index.html":
        main = re.sub(r'(?:<span>)?Acepto (?:que|el <a href="/privacidad">aviso de privacidad</a> y que) TRIBEROI use estos datos para responder mi mensaje\.(?:</span>)?', lambda m: PRIV_CHECK_LABEL, main)
        main = main.replace(f'<span>Dirección</span><span>{ORG["street"]}, {ORG["city"]} {ORG["postal"]}</span>',
                            f'<span>Dirección</span><span><a href="{ORG["maps_h"]}" target="_blank" rel="noopener">{ORG["street"]}, {ORG["city"]} {ORG["postal"]}</a></span>')
        main = main.replace('<span>Teléfono y WhatsApp</span><span><a href="https://wa.me/50230608643" target="_blank" rel="noopener">+502 3060 8643</a></span>',
                            f'<span>Teléfono y WhatsApp</span><span><a href="tel:{ORG["tel"]}">{ORG["tel_h"]}</a> <a class="mini" href="{ORG["wa"]}" target="_blank" rel="noopener">Abrir WhatsApp</a></span>')
        if "class=\"map\"" not in main:
            main = main.replace('</section>\n', MAP_SECTION, 1) if main.count('</section>') else main
    if key == "servicios/index.html" and 'id="preguntas"' not in main:
        faq = ('<section id="preguntas">\n  <div class="wrap faq">\n    <div class="sec-head" style="margin-bottom:0"><h2>Preguntas sobre nuestros servicios</h2>'
               '<p class="lead">Lo que conviene saber antes de contratar.</p></div>\n    ' + faq_html(SVC_FAQ) + '\n  </div>\n</section>\n')
        main = main.replace('<section class="band skyband">', faq + '<section class="band skyband">', 1)
    return main


MAP_SECTION = f"""</section>
<section class="white map-sec" aria-labelledby="mapa-t">
  <div class="wrap map-wrap">
    <div><h2 id="mapa-t">Cómo llegar</h2><p class="lead">{ORG['street']}, {ORG['city']} {ORG['postal']}. Horario de atención: lunes a viernes, de 8:00 a 17:00.</p><p><a class="textlink" href="{ORG['maps_h']}" target="_blank" rel="noopener">Abrir en Google Maps</a></p></div>
    <div class="map"><iframe title="Mapa de la oficina de TRIBEROI en la zona 15 de la Ciudad de Guatemala" src="https://www.google.com/maps?q=25+avenida+1-89+zona+15+Ciudad+de+Guatemala&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>
"""

PRIVACY_MAIN = f"""
<div class="page-intro">
  <div class="wrap">
    <p class="crumbs"><a href="/">Inicio</a> / Aviso de privacidad</p>
    <h1>Aviso de privacidad</h1>
    <p class="lead">Última actualización: 25 de octubre de 2026.</p>
  </div>
</div>
<section class="white">
  <div class="wrap prose">
    <h2>Quién es responsable de tus datos</h2>
    <p>{ORG['legal']}, con oficina en {ORG['street']}, {ORG['city']}, Guatemala. Para cualquier consulta sobre este aviso puedes escribir a <a href="mailto:{ORG['email']}">{ORG['email']}</a>.</p>
    <h2>Qué datos recibimos</h2>
    <p>Solo los que tú nos compartes al escribirnos por el formulario, correo o WhatsApp: nombre, correo, empresa, teléfono y el mensaje que nos envías.</p>
    <h2>Para qué los usamos</h2>
    <p>Para responder tu consulta, preparar una propuesta si la pides y darte seguimiento. No vendemos ni compartimos tus datos con terceros para fines publicitarios.</p>
    <h2>Cuánto tiempo los guardamos</h2>
    <p>Mientras sea necesario para atender tu solicitud o mantener la relación comercial. Si no llegamos a trabajar juntos, puedes pedirnos que los eliminemos en cualquier momento.</p>
    <h2>Tus derechos</h2>
    <p>Puedes pedirnos acceso, corrección o eliminación de tus datos escribiendo a <a href="mailto:{ORG['email']}">{ORG['email']}</a>. Te respondemos en un plazo razonable.</p>
    <h2>Cookies</h2>
    <p>Este sitio no usa cookies de publicidad ni de seguimiento. El mapa de la página de contacto lo provee Google Maps, que puede aplicar sus propias políticas cuando lo usas.</p>
    <h2>Cambios a este aviso</h2>
    <p>Si actualizamos este aviso, publicaremos la nueva versión en esta misma página con su fecha de actualización.</p>
  </div>
</section>
"""

NOTFOUND_MAIN = """
<section class="nf">
  <div class="wrap">
    <p class="nf-code" aria-hidden="true">404</p>
    <h1>No encontramos esta página</h1>
    <p class="lead">Puede que la dirección haya cambiado o tenga un error. Estas páginas sí existen:</p>
    <p class="nf-links"><a class="btn btn-ink" href="/">Ir al inicio</a><a class="btn btn-ghost" href="/servicios">Ver servicios</a><a class="btn btn-ghost" href="/contacto">Contacto</a></p>
  </div>
</section>
"""


def main():
    for key, p in PAGES.items():
        if key == "privacidad/index.html":
            body = PRIVACY_MAIN
        elif key == "404.html":
            body = NOTFOUND_MAIN
        else:
            body = transform(key, get_main(key))
        out = head(key, p) + "\n" + header(p) + '\n<main id="contenido">' + body + "</main>\n" + FOOTER
        dest = ROOT / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
        print("ok", key)


if __name__ == "__main__":
    main()
