'use strict';
function cents(value) {
  const s=String(value).trim();
  if (!/^\d{1,12}(?:[,.]\d{1,2})?$/.test(s)) throw new Error('Informe valores não negativos, sem separador de milhares, com até duas casas decimais.');
  const [whole,fraction='']=s.replace(',','.').split('.');
  return BigInt(whole)*100n+BigInt(fraction.padEnd(2,'0'));
}
function simulate(values) {
  const [r,c,t,a,e]=['revenue','costs','tax','alt','extra'].map(k=>cents(values[k]));
  const base=r-c-t, alternative=r-c-a-e, gain=alternative-base;
  return {base,alternative,gain,annual:gain*12n};
}
function brl(n) {
  const sign=n<0n?'-':'', abs=n<0n?-n:n;
  return sign+'R$ '+(abs/100n).toLocaleString('pt-BR')+','+String(abs%100n).padStart(2,'0');
}
if(typeof module!=='undefined') module.exports={cents,simulate,brl};
if(typeof document!=='undefined') {
  const form=document.getElementById('sim'), error=document.getElementById('error');
  function render() {
    try {
      const result=simulate(Object.fromEntries(new FormData(form)));
      for(const [id,value] of Object.entries(result)) document.getElementById(id).textContent=brl(value);
      error.textContent='';
    } catch(e) {
      error.textContent=e.message;
      for(const id of ['base','alternative','gain','annual']) document.getElementById(id).textContent='—';
    }
  }
  form.addEventListener('submit',e=>{e.preventDefault();render()});
  const button=document.getElementById('compare');
  button.addEventListener('click',()=>{if(form.reportValidity()) render()});
  button.disabled=false;
  render();
}
