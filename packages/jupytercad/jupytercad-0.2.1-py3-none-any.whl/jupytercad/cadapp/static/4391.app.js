"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[4391],{4391:(t,e,n)=>{function r(t){for(var e={},n=0;n<t.length;++n)e[t[n]]=!0;return e}n.r(e),n.d(e,{r:()=>b});var a,i=["NULL","NA","Inf","NaN","NA_integer_","NA_real_","NA_complex_","NA_character_","TRUE","FALSE"],c=["list","quote","bquote","eval","return","call","parse","deparse"],o=["if","else","repeat","while","function","for","in","next","break"],l=r(i),u=r(c),f=r(o),s=r(["if","else","repeat","while","function","for"]),p=/[+\-*\/^<>=!&|~$:]/;function m(t,e){a=null;var n,r=t.next();if("#"==r)return t.skipToEnd(),"comment";if("0"==r&&t.eat("x"))return t.eatWhile(/[\da-f]/i),"number";if("."==r&&t.eat(/\d/))return t.match(/\d*(?:e[+\-]?\d+)?/),"number";if(/\d/.test(r))return t.match(/\d*(?:\.\d+)?(?:e[+\-]\d+)?L?/),"number";if("'"==r||'"'==r)return e.tokenize=(n=r,function(t,e){if(t.eat("\\")){var r=t.next();return"x"==r?t.match(/^[a-f0-9]{2}/i):("u"==r||"U"==r)&&t.eat("{")&&t.skipTo("}")?t.next():"u"==r?t.match(/^[a-f0-9]{4}/i):"U"==r?t.match(/^[a-f0-9]{8}/i):/[0-7]/.test(r)&&t.match(/^[0-7]{1,2}/),"string.special"}for(var a;null!=(a=t.next());){if(a==n){e.tokenize=m;break}if("\\"==a){t.backUp(1);break}}return"string"}),"string";if("`"==r)return t.match(/[^`]+`/),"string.special";if("."==r&&t.match(/.(?:[.]|\d+)/))return"keyword";if(/[a-zA-Z\.]/.test(r)){t.eatWhile(/[\w\.]/);var i=t.current();return l.propertyIsEnumerable(i)?"atom":f.propertyIsEnumerable(i)?(s.propertyIsEnumerable(i)&&!t.match(/\s*if(\s+|$)/,!1)&&(a="block"),"keyword"):u.propertyIsEnumerable(i)?"builtin":"variable"}return"%"==r?(t.skipTo("%")&&t.next(),"variableName.special"):"<"==r&&t.eat("-")||"<"==r&&t.match("<-")||"-"==r&&t.match(/>>?/)||"="==r&&e.ctx.argList?"operator":p.test(r)?("$"==r||t.eatWhile(p),"operator"):/[\(\){}\[\];]/.test(r)?(a=r,";"==r?"punctuation":null):null}function d(t,e,n){t.ctx={type:e,indent:t.indent,flags:0,column:n.column(),prev:t.ctx}}function k(t,e){var n=t.ctx;t.ctx={type:n.type,indent:n.indent,flags:n.flags|e,column:n.column,prev:n.prev}}function x(t){t.indent=t.ctx.indent,t.ctx=t.ctx.prev}const b={name:"r",startState:function(t){return{tokenize:m,ctx:{type:"top",indent:-t,flags:2},indent:0,afterIdent:!1}},token:function(t,e){if(t.sol()&&(0==(3&e.ctx.flags)&&(e.ctx.flags|=2),4&e.ctx.flags&&x(e),e.indent=t.indentation()),t.eatSpace())return null;var n=e.tokenize(t,e);return"comment"!=n&&0==(2&e.ctx.flags)&&k(e,1),";"!=a&&"{"!=a&&"}"!=a||"block"!=e.ctx.type||x(e),"{"==a?d(e,"}",t):"("==a?(d(e,")",t),e.afterIdent&&(e.ctx.argList=!0)):"["==a?d(e,"]",t):"block"==a?d(e,"block",t):a==e.ctx.type?x(e):"block"==e.ctx.type&&"comment"!=n&&k(e,4),e.afterIdent="variable"==n||"keyword"==n,n},indent:function(t,e,n){if(t.tokenize!=m)return 0;var r=e&&e.charAt(0),a=t.ctx,i=r==a.type;return 4&a.flags&&(a=a.prev),"block"==a.type?a.indent+("{"==r?0:n.unit):1&a.flags?a.column+(i?0:1):a.indent+(i?0:n.unit)},languageData:{wordChars:".",commentTokens:{line:"#"},autocomplete:i.concat(c,o)}}}}]);