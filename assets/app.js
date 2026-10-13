(function(){
  /* Menú en celular */
  var nav = document.getElementById('nav'), btn = document.getElementById('menuBtn');
  if(btn) btn.addEventListener('click', function(){
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* Borde del encabezado al hacer scroll */
  var top = document.querySelector('.top');
  function onScroll(){ if(top) top.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  /* Si una foto no carga, se muestra el símbolo de la marca */
  document.querySelectorAll('.photo img').forEach(function(img){
    function fail(){ img.parentNode.classList.add('noimg'); }
    if(img.complete && img.naturalWidth === 0) fail();
    img.addEventListener('error', fail);
  });

  /* Explorador de servicios */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function select(tab, focus){
    tabs.forEach(function(t){
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var p = document.getElementById(t.getAttribute('aria-controls'));
      if(p){ p.hidden = !on; if(on){ p.classList.remove('enter'); void p.offsetWidth; p.classList.add('enter'); } }
    });
    if(focus) tab.focus();
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ select(t); });
    t.addEventListener('keydown', function(e){
      if(e.key === 'ArrowDown' || e.key === 'ArrowRight'){ e.preventDefault(); select(tabs[(i + 1) % tabs.length], true); }
      if(e.key === 'ArrowUp' || e.key === 'ArrowLeft'){ e.preventDefault(); select(tabs[(i - 1 + tabs.length) % tabs.length], true); }
    });
  });

  /* Servicio preseleccionado desde otro enlace: /contacto?servicio=... */
  try{
    var s = new URLSearchParams(location.search).get('servicio');
    var sel = document.getElementById('c-servicio');
    if(s && sel){ Array.prototype.forEach.call(sel.options, function(o){ if(o.value === s) sel.value = s; }); }
  }catch(e){}

  /* Formularios: validación y confirmación (el envío real se conecta al correo de TRIBEROI) */
  document.querySelectorAll('form[data-form]').forEach(function(f){
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var old = f.querySelector('.form-msg'); if(old) old.remove();
      var missing = Array.prototype.filter.call(f.querySelectorAll('[required]'), function(el){
        return el.type === 'checkbox' ? !el.checked : !el.value.trim();
      });
      var msg = document.createElement('p');
      msg.setAttribute('role','status');
      if(missing.length){
        msg.className = 'form-msg err';
        msg.textContent = 'Falta completar: ' + missing.map(function(el){
          var l = f.querySelector('label[for="' + el.id + '"]'); return l ? l.textContent.replace(/\s*\*$/,'').trim() : el.name;
        }).join(', ') + '.';
        missing[0].focus();
      } else {
        msg.className = 'form-msg ok';
        msg.textContent = 'Gracias, recibimos tu mensaje. Una persona de nuestro equipo te va a escribir pronto.';
        f.reset();
      }
      f.appendChild(msg);
    });
  });
})();
