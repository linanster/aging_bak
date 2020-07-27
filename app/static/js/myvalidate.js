function validate_required(field,alerttxt)
{
with (field)
  {
  if (value==null||value=="")
    {alert(alerttxt);return false}
  else {return true}
  }
}

function validate_format_fwversion(field,alerttxt)
{
with (field)
  {
    var macReg=/^[1-9][0-9]{4}$/;
    if (macReg.test(value))
      {return true}
    else if (value.length == 0)
      {return true}
    else
      {alert(alerttxt);return false}
  }
}

function validate_format_mac(field,alerttxt)
{
with (field)
  {
    if (value.length == 0)
      {return true}
    var macReg=/[0-9a-zA-Z]{12}/;
    if (macReg.test(value))
      {return true}
    else
      {alert(alerttxt);return false}
  }
}

function validate_form(thisform)
{
with (thisform)
  {
  if (validate_required(devicecode,"请选择设备类型!")==false)
    {devicecode.focus();return false}
   
  if (validate_required(totalcount,"请选择设备数量!")==false)
    {totalcount.focus();return false}
   
   if (validate_required(fwversion,"请输入固件版本号!")==false)
     {fwversion.focus();return false}
   
  if (validate_format_fwversion(fwversion,"固件版本号格式错误!")==false)
    {fwversion.focus();return false}
  if (validate_format_mac(wifi_mac_low,"wifi_mac_low 格式错误!")==false)
    {wifi_mac_low.focus();return false}
  if (validate_format_mac(wifi_mac_high,"wifi_mac_high 格式错误!")==false)
    {wifi_mac_high.focus();return false}
  if (validate_format_mac(ble_mac_low,"ble_mac_low 格式错误!")==false)
    {ble_mac_low.focus();return false}
  if (validate_format_mac(ble_mac_high,"ble_mac_high 格式错误!")==false)
    {ble_mac_high.focus();return false}
  }
}

