"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[7058],{27058:(T,O,E)=>{function I(T){for(var O={},E=T.split(" "),I=0;I<E.length;++I)O[E[I]]=!0;return O}E.r(O),E.d(O,{pig:()=>C});var N="ABS ACOS ARITY ASIN ATAN AVG BAGSIZE BINSTORAGE BLOOM BUILDBLOOM CBRT CEIL CONCAT COR COS COSH COUNT COUNT_STAR COV CONSTANTSIZE CUBEDIMENSIONS DIFF DISTINCT DOUBLEABS DOUBLEAVG DOUBLEBASE DOUBLEMAX DOUBLEMIN DOUBLEROUND DOUBLESUM EXP FLOOR FLOATABS FLOATAVG FLOATMAX FLOATMIN FLOATROUND FLOATSUM GENERICINVOKER INDEXOF INTABS INTAVG INTMAX INTMIN INTSUM INVOKEFORDOUBLE INVOKEFORFLOAT INVOKEFORINT INVOKEFORLONG INVOKEFORSTRING INVOKER ISEMPTY JSONLOADER JSONMETADATA JSONSTORAGE LAST_INDEX_OF LCFIRST LOG LOG10 LOWER LONGABS LONGAVG LONGMAX LONGMIN LONGSUM MAX MIN MAPSIZE MONITOREDUDF NONDETERMINISTIC OUTPUTSCHEMA  PIGSTORAGE PIGSTREAMING RANDOM REGEX_EXTRACT REGEX_EXTRACT_ALL REPLACE ROUND SIN SINH SIZE SQRT STRSPLIT SUBSTRING SUM STRINGCONCAT STRINGMAX STRINGMIN STRINGSIZE TAN TANH TOBAG TOKENIZE TOMAP TOP TOTUPLE TRIM TEXTLOADER TUPLESIZE UCFIRST UPPER UTF8STORAGECONVERTER ",A="VOID IMPORT RETURNS DEFINE LOAD FILTER FOREACH ORDER CUBE DISTINCT COGROUP JOIN CROSS UNION SPLIT INTO IF OTHERWISE ALL AS BY USING INNER OUTER ONSCHEMA PARALLEL PARTITION GROUP AND OR NOT GENERATE FLATTEN ASC DESC IS STREAM THROUGH STORE MAPREDUCE SHIP CACHE INPUT OUTPUT STDERROR STDIN STDOUT LIMIT SAMPLE LEFT RIGHT FULL EQ GT LT GTE LTE NEQ MATCHES TRUE FALSE DUMP",e="BOOLEAN INT LONG FLOAT DOUBLE CHARARRAY BYTEARRAY BAG TUPLE MAP ",R=I(N),S=I(A),t=I(e),L=/[*+\-%<>=&?:\/!|]/;function r(T,O,E){return O.tokenize=E,E(T,O)}function U(T,O){for(var E,I=!1;E=T.next();){if("/"==E&&I){O.tokenize=n;break}I="*"==E}return"comment"}function n(T,O){var E,I=T.next();return'"'==I||"'"==I?r(T,O,(E=I,function(T,O){for(var I,N=!1,A=!1;null!=(I=T.next());){if(I==E&&!N){A=!0;break}N=!N&&"\\"==I}return!A&&N||(O.tokenize=n),"error"})):/[\[\]{}\(\),;\.]/.test(I)?null:/\d/.test(I)?(T.eatWhile(/[\w\.]/),"number"):"/"==I?T.eat("*")?r(T,O,U):(T.eatWhile(L),"operator"):"-"==I?T.eat("-")?(T.skipToEnd(),"comment"):(T.eatWhile(L),"operator"):L.test(I)?(T.eatWhile(L),"operator"):(T.eatWhile(/[\w\$_]/),S&&S.propertyIsEnumerable(T.current().toUpperCase())&&!T.eat(")")&&!T.eat(".")?"keyword":R&&R.propertyIsEnumerable(T.current().toUpperCase())?"builtin":t&&t.propertyIsEnumerable(T.current().toUpperCase())?"type":"variable")}const C={name:"pig",startState:function(){return{tokenize:n,startOfLine:!0}},token:function(T,O){return T.eatSpace()?null:O.tokenize(T,O)},languageData:{autocomplete:(N+e+A).split(" ")}}}}]);