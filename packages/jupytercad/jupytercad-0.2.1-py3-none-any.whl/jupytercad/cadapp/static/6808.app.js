"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[6808],{36808:(t,n,r)=>{var e;function i(t){return"function"==typeof t.iter?t.iter():new _(t)}function o(t){return new p(t)}function u(t){return new x(t)}function a(t){return new l(t)}function h(t){return new m(t)}function f(t,n){for(var r,e=0,o=i(t);void 0!==(r=o.next());)if(!1===n(r,e++))return}function c(t,n){for(var r,e=0,o=i(t);void 0!==(r=o.next());)if(!n(r,e++))return!1;return!0}function s(t,n){for(var r,e=0,o=i(t);void 0!==(r=o.next());)if(n(r,e++))return!0;return!1}function v(t){for(var n,r=0,e=[],o=i(t);void 0!==(n=o.next());)e[r++]=n;return e}function d(t){for(var n,r=i(t),e={};void 0!==(n=r.next());)e[n[0]]=n[1];return e}r.r(n),r.d(n,{ArrayExt:()=>e,ArrayIterator:()=>_,ChainIterator:()=>M,EmptyIterator:()=>w,EnumerateIterator:()=>k,FilterIterator:()=>E,FnIterator:()=>m,ItemIterator:()=>l,KeyIterator:()=>p,MapIterator:()=>T,RangeIterator:()=>j,RepeatIterator:()=>W,RetroArrayIterator:()=>z,StrideIterator:()=>D,StringExt:()=>Y,TakeIterator:()=>G,ValueIterator:()=>x,ZipIterator:()=>N,chain:()=>y,each:()=>f,empty:()=>g,enumerate:()=>I,every:()=>c,filter:()=>O,find:()=>A,findIndex:()=>b,iter:()=>i,iterFn:()=>h,iterItems:()=>a,iterKeys:()=>o,iterValues:()=>u,map:()=>S,max:()=>L,min:()=>F,minmax:()=>R,once:()=>V,range:()=>U,reduce:()=>B,repeat:()=>P,retro:()=>q,some:()=>s,stride:()=>K,take:()=>Z,toArray:()=>v,toObject:()=>d,topologicSort:()=>J,zip:()=>H}),function(t){function n(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i,o=t.length;if(0===o)return-1;r=r<0?Math.max(0,r+o):Math.min(r,o-1),i=(e=e<0?Math.max(0,e+o):Math.min(e,o-1))<r?e+1+(o-r):e-r+1;for(var u=0;u<i;++u){var a=(r+u)%o;if(t[a]===n)return a}return-1}function r(t,n,r,e){void 0===r&&(r=-1),void 0===e&&(e=0);var i,o=t.length;if(0===o)return-1;i=(r=r<0?Math.max(0,r+o):Math.min(r,o-1))<(e=e<0?Math.max(0,e+o):Math.min(e,o-1))?r+1+(o-e):r-e+1;for(var u=0;u<i;++u){var a=(r-u+o)%o;if(t[a]===n)return a}return-1}function e(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i,o=t.length;if(0===o)return-1;r=r<0?Math.max(0,r+o):Math.min(r,o-1),i=(e=e<0?Math.max(0,e+o):Math.min(e,o-1))<r?e+1+(o-r):e-r+1;for(var u=0;u<i;++u){var a=(r+u)%o;if(n(t[a],a))return a}return-1}function i(t,n,r,e){void 0===r&&(r=-1),void 0===e&&(e=0);var i,o=t.length;if(0===o)return-1;i=(r=r<0?Math.max(0,r+o):Math.min(r,o-1))<(e=e<0?Math.max(0,e+o):Math.min(e,o-1))?r+1+(o-e):r-e+1;for(var u=0;u<i;++u){var a=(r-u+o)%o;if(n(t[a],a))return a}return-1}function o(t,n,r){void 0===n&&(n=0),void 0===r&&(r=-1);var e=t.length;if(!(e<=1))for(n=n<0?Math.max(0,n+e):Math.min(n,e-1),r=r<0?Math.max(0,r+e):Math.min(r,e-1);n<r;){var i=t[n],o=t[r];t[n++]=o,t[r--]=i}}function u(t,n){var r=t.length;if(n<0&&(n+=r),!(n<0||n>=r)){for(var e=t[n],i=n+1;i<r;++i)t[i-1]=t[i];return t.length=r-1,e}}t.firstIndexOf=n,t.lastIndexOf=r,t.findFirstIndex=e,t.findLastIndex=i,t.findFirstValue=function(t,n,r,i){void 0===r&&(r=0),void 0===i&&(i=-1);var o=e(t,n,r,i);return-1!==o?t[o]:void 0},t.findLastValue=function(t,n,r,e){void 0===r&&(r=-1),void 0===e&&(e=0);var o=i(t,n,r,e);return-1!==o?t[o]:void 0},t.lowerBound=function(t,n,r,e,i){void 0===e&&(e=0),void 0===i&&(i=-1);var o=t.length;if(0===o)return 0;for(var u=e=e<0?Math.max(0,e+o):Math.min(e,o-1),a=(i=i<0?Math.max(0,i+o):Math.min(i,o-1))-e+1;a>0;){var h=a>>1,f=u+h;r(t[f],n)<0?(u=f+1,a-=h+1):a=h}return u},t.upperBound=function(t,n,r,e,i){void 0===e&&(e=0),void 0===i&&(i=-1);var o=t.length;if(0===o)return 0;for(var u=e=e<0?Math.max(0,e+o):Math.min(e,o-1),a=(i=i<0?Math.max(0,i+o):Math.min(i,o-1))-e+1;a>0;){var h=a>>1,f=u+h;r(t[f],n)>0?a=h:(u=f+1,a-=h+1)}return u},t.shallowEqual=function(t,n,r){if(t===n)return!0;if(t.length!==n.length)return!1;for(var e=0,i=t.length;e<i;++e)if(r?!r(t[e],n[e]):t[e]!==n[e])return!1;return!0},t.slice=function(t,n){void 0===n&&(n={});var r=n.start,e=n.stop,i=n.step;if(void 0===i&&(i=1),0===i)throw new Error("Slice `step` cannot be zero.");var o,u=t.length;void 0===r?r=i<0?u-1:0:r<0?r=Math.max(r+u,i<0?-1:0):r>=u&&(r=i<0?u-1:u),void 0===e?e=i<0?-1:u:e<0?e=Math.max(e+u,i<0?-1:0):e>=u&&(e=i<0?u-1:u),o=i<0&&e>=r||i>0&&r>=e?0:i<0?Math.floor((e-r+1)/i+1):Math.floor((e-r-1)/i+1);for(var a=[],h=0;h<o;++h)a[h]=t[r+h*i];return a},t.move=function(t,n,r){var e=t.length;if(!(e<=1)&&(n=n<0?Math.max(0,n+e):Math.min(n,e-1))!==(r=r<0?Math.max(0,r+e):Math.min(r,e-1))){for(var i=t[n],o=n<r?1:-1,u=n;u!==r;u+=o)t[u]=t[u+o];t[r]=i}},t.reverse=o,t.rotate=function(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i=t.length;if(!(i<=1||(r=r<0?Math.max(0,r+i):Math.min(r,i-1))>=(e=e<0?Math.max(0,e+i):Math.min(e,i-1)))){var u=e-r+1;if(n>0?n%=u:n<0&&(n=(n%u+u)%u),0!==n){var a=r+n;o(t,r,a-1),o(t,a,e),o(t,r,e)}}},t.fill=function(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i=t.length;if(0!==i){var o;r=r<0?Math.max(0,r+i):Math.min(r,i-1),o=(e=e<0?Math.max(0,e+i):Math.min(e,i-1))<r?e+1+(i-r):e-r+1;for(var u=0;u<o;++u)t[(r+u)%i]=n}},t.insert=function(t,n,r){var e=t.length;n=n<0?Math.max(0,n+e):Math.min(n,e);for(var i=e;i>n;--i)t[i]=t[i-1];t[n]=r},t.removeAt=u,t.removeFirstOf=function(t,r,e,i){void 0===e&&(e=0),void 0===i&&(i=-1);var o=n(t,r,e,i);return-1!==o&&u(t,o),o},t.removeLastOf=function(t,n,e,i){void 0===e&&(e=-1),void 0===i&&(i=0);var o=r(t,n,e,i);return-1!==o&&u(t,o),o},t.removeAllOf=function(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i=t.length;if(0===i)return 0;r=r<0?Math.max(0,r+i):Math.min(r,i-1),e=e<0?Math.max(0,e+i):Math.min(e,i-1);for(var o=0,u=0;u<i;++u)r<=e&&u>=r&&u<=e&&t[u]===n||e<r&&(u<=e||u>=r)&&t[u]===n?o++:o>0&&(t[u-o]=t[u]);return o>0&&(t.length=i-o),o},t.removeFirstWhere=function(t,n,r,i){var o;void 0===r&&(r=0),void 0===i&&(i=-1);var a=e(t,n,r,i);return-1!==a&&(o=u(t,a)),{index:a,value:o}},t.removeLastWhere=function(t,n,r,e){var o;void 0===r&&(r=-1),void 0===e&&(e=0);var a=i(t,n,r,e);return-1!==a&&(o=u(t,a)),{index:a,value:o}},t.removeAllWhere=function(t,n,r,e){void 0===r&&(r=0),void 0===e&&(e=-1);var i=t.length;if(0===i)return 0;r=r<0?Math.max(0,r+i):Math.min(r,i-1),e=e<0?Math.max(0,e+i):Math.min(e,i-1);for(var o=0,u=0;u<i;++u)r<=e&&u>=r&&u<=e&&n(t[u],u)||e<r&&(u<=e||u>=r)&&n(t[u],u)?o++:o>0&&(t[u-o]=t[u]);return o>0&&(t.length=i-o),o}}(e||(e={}));var _=function(){function t(t){this._index=0,this._source=t}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index>=this._source.length))return this._source[this._index++]},t}(),p=function(){function t(t,n){void 0===n&&(n=Object.keys(t)),this._index=0,this._source=t,this._keys=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source,this._keys);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index>=this._keys.length)){var t=this._keys[this._index++];return t in this._source?t:this.next()}},t}(),x=function(){function t(t,n){void 0===n&&(n=Object.keys(t)),this._index=0,this._source=t,this._keys=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source,this._keys);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index>=this._keys.length)){var t=this._keys[this._index++];return t in this._source?this._source[t]:this.next()}},t}(),l=function(){function t(t,n){void 0===n&&(n=Object.keys(t)),this._index=0,this._source=t,this._keys=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source,this._keys);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index>=this._keys.length)){var t=this._keys[this._index++];return t in this._source?[t,this._source[t]]:this.next()}},t}(),m=function(){function t(t){this._fn=t}return t.prototype.iter=function(){return this},t.prototype.clone=function(){throw new Error("An `FnIterator` cannot be cloned.")},t.prototype.next=function(){return this._fn.call(void 0)},t}();function y(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];return new M(i(t.map(i)))}var M=function(){function t(t){this._cloned=!1,this._source=t,this._active=void 0}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source.clone());return n._active=this._active&&this._active.clone(),n._cloned=!0,this._cloned=!0,n},t.prototype.next=function(){if(void 0===this._active){var t=this._source.next();if(void 0===t)return;this._active=this._cloned?t.clone():t}var n=this._active.next();return void 0!==n?n:(this._active=void 0,this.next())},t}();function g(){return new w}var w=function(){function t(){}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t},t.prototype.next=function(){},t}();function I(t,n){return void 0===n&&(n=0),new k(i(t),n)}var k=function(){function t(t,n){this._source=t,this._index=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t(this._source.clone(),this._index)},t.prototype.next=function(){var t=this._source.next();if(void 0!==t)return[this._index++,t]},t}();function O(t,n){return new E(i(t),n)}var E=function(){function t(t,n){this._index=0,this._source=t,this._fn=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source.clone(),this._fn);return n._index=this._index,n},t.prototype.next=function(){for(var t,n=this._fn,r=this._source;void 0!==(t=r.next());)if(n(t,this._index++))return t},t}();function A(t,n){for(var r,e=0,o=i(t);void 0!==(r=o.next());)if(n(r,e++))return r}function b(t,n){for(var r,e=0,o=i(t);void 0!==(r=o.next());)if(n(r,e++))return e-1;return-1}function F(t,n){var r=i(t),e=r.next();if(void 0!==e){for(var o=e;void 0!==(e=r.next());)n(e,o)<0&&(o=e);return o}}function L(t,n){var r=i(t),e=r.next();if(void 0!==e){for(var o=e;void 0!==(e=r.next());)n(e,o)>0&&(o=e);return o}}function R(t,n){var r=i(t),e=r.next();if(void 0!==e){for(var o=e,u=e;void 0!==(e=r.next());)n(e,o)<0?o=e:n(e,u)>0&&(u=e);return[o,u]}}function S(t,n){return new T(i(t),n)}var T=function(){function t(t,n){this._index=0,this._source=t,this._fn=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source.clone(),this._fn);return n._index=this._index,n},t.prototype.next=function(){var t=this._source.next();if(void 0!==t)return this._fn.call(void 0,t,this._index++)},t}();function U(t,n,r){return void 0===n?new j(0,t,1):new j(t,n,void 0===r?1:r)}var C,j=function(){function t(t,n,r){this._index=0,this._start=t,this._stop=n,this._step=r,this._length=C.rangeLength(t,n,r)}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._start,this._stop,this._step);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index>=this._length))return this._start+this._step*this._index++},t}();function B(t,n,r){var e=0,o=i(t),u=o.next();if(void 0===u&&void 0===r)throw new TypeError("Reduce of empty iterable with no initial value.");if(void 0===u)return r;var a,h,f=o.next();if(void 0===f&&void 0===r)return u;if(void 0===f)return n(r,u,e++);for(a=n(void 0===r?u:n(r,u,e++),f,e++);void 0!==(h=o.next());)a=n(a,h,e++);return a}function P(t,n){return new W(t,n)}function V(t){return new W(t,1)}!function(t){t.rangeLength=function(t,n,r){return 0===r?1/0:t>n&&r>0||t<n&&r<0?0:Math.ceil((n-t)/r)}}(C||(C={}));var W=function(){function t(t,n){this._value=t,this._count=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t(this._value,this._count)},t.prototype.next=function(){if(!(this._count<=0))return this._count--,this._value},t}();function q(t){return"function"==typeof t.retro?t.retro():new z(t)}var z=function(){function t(t){this._source=t,this._index=t.length-1}return t.prototype.iter=function(){return this},t.prototype.clone=function(){var n=new t(this._source);return n._index=this._index,n},t.prototype.next=function(){if(!(this._index<0||this._index>=this._source.length))return this._source[this._index--]},t}();function J(t){var n=[],r=new Set,e=new Map;return f(t,(function(t){var n=t[0],r=t[1],i=e.get(r);i?i.push(n):e.set(r,[n])})),e.forEach((function(t,n){i(n)})),n;function i(t){if(!r.has(t)){r.add(t);var o=e.get(t);o&&o.forEach(i),n.push(t)}}}function K(t,n){return new D(i(t),n)}var Y,D=function(){function t(t,n){this._source=t,this._step=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t(this._source.clone(),this._step)},t.prototype.next=function(){for(var t=this._source.next(),n=this._step-1;n>0;--n)this._source.next();return t},t}();function Z(t,n){return new G(i(t),n)}!function(t){function n(t,n,r){void 0===r&&(r=0);for(var e=new Array(n.length),i=0,o=r,u=n.length;i<u;++i,++o){if(-1===(o=t.indexOf(n[i],o)))return null;e[i]=o}return e}t.findIndices=n,t.matchSumOfSquares=function(t,r,e){void 0===e&&(e=0);var i=n(t,r,e);if(!i)return null;for(var o=0,u=0,a=i.length;u<a;++u){var h=i[u]-e;o+=h*h}return{score:o,indices:i}},t.matchSumOfDeltas=function(t,r,e){void 0===e&&(e=0);var i=n(t,r,e);if(!i)return null;for(var o=0,u=e-1,a=0,h=i.length;a<h;++a){var f=i[a];o+=f-u-1,u=f}return{score:o,indices:i}},t.highlight=function(t,n,r){for(var e=[],i=0,o=0,u=n.length;i<u;){for(var a=n[i],h=n[i];++i<u&&n[i]===h+1;)h++;o<a&&e.push(t.slice(o,a)),a<h+1&&e.push(r(t.slice(a,h+1))),o=h+1}return o<t.length&&e.push(t.slice(o)),e},t.cmp=function(t,n){return t<n?-1:t>n?1:0}}(Y||(Y={}));var G=function(){function t(t,n){this._source=t,this._count=n}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t(this._source.clone(),this._count)},t.prototype.next=function(){if(!(this._count<=0)){var t=this._source.next();if(void 0!==t)return this._count--,t}},t}();function H(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];return new N(t.map(i))}var N=function(){function t(t){this._source=t}return t.prototype.iter=function(){return this},t.prototype.clone=function(){return new t(this._source.map((function(t){return t.clone()})))},t.prototype.next=function(){for(var t=new Array(this._source.length),n=0,r=this._source.length;n<r;++n){var e=this._source[n].next();if(void 0===e)return;t[n]=e}return t},t}()}}]);