# Polyfill
if !'remove' of Element.prototype
  Element.prototype.remove = !->
    if this.parentNode
      this.parentNode.removeChild this

# 首页
do !->
  input = document.getElementById 'name'
  btn = document.querySelector 'form button[type=submit]'
  if !btn || !input
    return

  # 初始设置按钮是否可点击
  btn.disabled = /^\s*$/.test input.value

  # 姓名不为空时按钮才能点击
  if 'oninput' of input
    input.oninput = !->
      btn.disabled = /^\s*$/.test this.value
  else
    input.onkeyup = !->
      btn.disabled = /^\s*$/.test this.value

  document.querySelector 'form' .onsubmit = (event)!->
    if btn.disabled
      if event.preventDefaul
        event.preventDefaul!
      else
        event.returnValue = false

# 结果页
do !->
  btn = document.getElementById 'share-to-moment'
  shareMask = document.querySelector '.share-mask'
  if !btn || !shareMask
    return

  if !/MicroMessenge/i.test window.navigator.userAgent
    shareMask.classList.add 'not-in-wechat'

  btn.onclick = !->
    shareMask.classList.add 'active'

  shareMask.onclick = (event)!->
    if event.target == this or event.target.className == 'close'
      shareMask.classList.remove 'active'

# 设置页面底部二维码提示语
do !->
  if !/MicroMessenge/i.test window.navigator.userAgent
    document.querySelector '.qrcode .prompt' .classList.add 'not-in-wechat'
