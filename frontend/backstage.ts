export default function(){
  if (document.location.hash === "#go-backstage"){
    localStorage.setItem('backstage', 'y')
  }
  if (document.location.hash === "#leave-backstage"){
    localStorage.removeItem('backstage')
  }
  if (localStorage.getItem('backstage') !== null){
    document.body.classList.add('backstage')
  }
}