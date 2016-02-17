var class = ["due4605","zkossow","cplant","jarshea","pallav04","andreanboot","pradnyil","rkpoon22","lidaphd","sunnyma1990","apoorvamodali","rohan7293","rsibi","anistrju","ssanjhana15","yyan33"];

var prof = "pengyu.bio@gmail.com"

function generate_spreadSheet()
{
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  for(var student in class)
  {
    var new_sheet = ss.copy(ss.getName()+"_"+class[student]);
    new_sheet.addEditor(class[student] + "@tamu.edu");
    new_sheet.addEditor(prof);
  }
}
