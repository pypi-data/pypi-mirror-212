"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[3500],{43500:(e,t,n)=>{n.r(t),n.d(t,{vb:()=>z});var r="error";function a(e){return new RegExp("^(("+e.join(")|(")+"))\\b","i")}var i=new RegExp("^[\\+\\-\\*/%&\\\\|\\^~<>!]"),o=new RegExp("^[\\(\\)\\[\\]\\{\\}@,:`=;\\.]"),c=new RegExp("^((==)|(<>)|(<=)|(>=)|(<>)|(<<)|(>>)|(//)|(\\*\\*))"),s=new RegExp("^((\\+=)|(\\-=)|(\\*=)|(%=)|(/=)|(&=)|(\\|=)|(\\^=))"),u=new RegExp("^((//=)|(>>=)|(<<=)|(\\*\\*=))"),l=new RegExp("^[_A-Za-z][_A-Za-z0-9]*"),d=["class","module","sub","enum","select","while","if","function","get","set","property","try","structure","synclock","using","with"],m=["else","elseif","case","catch","finally"],h=["next","loop"],f=["and","andalso","or","orelse","xor","in","not","is","isnot","like"],p=a(f),b=["#const","#else","#elseif","#end","#if","#region","addhandler","addressof","alias","as","byref","byval","cbool","cbyte","cchar","cdate","cdbl","cdec","cint","clng","cobj","compare","const","continue","csbyte","cshort","csng","cstr","cuint","culng","cushort","declare","default","delegate","dim","directcast","each","erase","error","event","exit","explicit","false","for","friend","gettype","goto","handles","implements","imports","infer","inherits","interface","isfalse","istrue","lib","me","mod","mustinherit","mustoverride","my","mybase","myclass","namespace","narrowing","new","nothing","notinheritable","notoverridable","of","off","on","operator","option","optional","out","overloads","overridable","overrides","paramarray","partial","private","protected","public","raiseevent","readonly","redim","removehandler","resume","return","shadows","shared","static","step","stop","strict","then","throw","to","true","trycast","typeof","until","until","when","widening","withevents","writeonly"],g=["object","boolean","char","string","byte","sbyte","short","ushort","int16","uint16","integer","uinteger","int32","uint32","long","ulong","int64","uint64","decimal","single","double","float","date","datetime","intptr","uintptr"],k=a(b),y=a(g),v=a(d),w=a(m),x=a(h),I=a(["end"]),E=a(["do"]);function L(e,t){t.currentIndent++}function R(e,t){t.currentIndent--}function T(e,t){if(e.eatSpace())return null;var n,a,d;if("'"===e.peek())return e.skipToEnd(),"comment";if(e.match(/^((&H)|(&O))?[0-9\.a-f]/i,!1)){var m=!1;if((e.match(/^\d*\.\d+F?/i)||e.match(/^\d+\.\d*F?/)||e.match(/^\.\d+F?/))&&(m=!0),m)return e.eat(/J/i),"number";var h=!1;if(e.match(/^&H[0-9a-f]+/i)||e.match(/^&O[0-7]+/i)?h=!0:e.match(/^[1-9]\d*F?/)?(e.eat(/J/i),h=!0):e.match(/^0(?![\dx])/i)&&(h=!0),h)return e.eat(/L/i),"number"}return e.match('"')?(t.tokenize=(n=e.current(),a=1==n.length,d="string",function(e,t){for(;!e.eol();){if(e.eatWhile(/[^'"]/),e.match(n))return t.tokenize=T,d;e.eat(/['"]/)}return a&&(t.tokenize=T),d}),t.tokenize(e,t)):e.match(u)||e.match(s)?null:e.match(c)||e.match(i)||e.match(p)?"operator":e.match(o)?null:e.match(E)?(L(0,t),t.doInCurrentLine=!0,"keyword"):e.match(v)?(t.doInCurrentLine?t.doInCurrentLine=!1:L(0,t),"keyword"):e.match(w)?"keyword":e.match(I)?(R(0,t),R(0,t),"keyword"):e.match(x)?(R(0,t),"keyword"):e.match(y)||e.match(k)?"keyword":e.match(l)?"variable":(e.next(),r)}const z={name:"vb",startState:function(){return{tokenize:T,lastToken:null,currentIndent:0,nextLineIndent:0,doInCurrentLine:!1}},token:function(e,t){e.sol()&&(t.currentIndent+=t.nextLineIndent,t.nextLineIndent=0,t.doInCurrentLine=0);var n=function(e,t){var n=t.tokenize(e,t),a=e.current();if("."===a)return"variable"===(n=t.tokenize(e,t))?"variable":r;var i="[({".indexOf(a);return-1!==i&&L(0,t),-1!==(i="])}".indexOf(a))&&R(0,t)?r:n}(e,t);return t.lastToken={style:n,content:e.current()},n},indent:function(e,t,n){var r=t.replace(/^\s+|\s+$/g,"");return r.match(x)||r.match(I)||r.match(w)?n.unit*(e.currentIndent-1):e.currentIndent<0?0:e.currentIndent*n.unit},languageData:{closeBrackets:{brackets:["(","[","{",'"']},commentTokens:{line:"'"},autocomplete:d.concat(m).concat(h).concat(f).concat(b).concat(g)}}}}]);