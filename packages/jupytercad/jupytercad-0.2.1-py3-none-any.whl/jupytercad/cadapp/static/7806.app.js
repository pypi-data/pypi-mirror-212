"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[7806,8518],{18518:(t,e,i)=>{i.r(e),i.d(e,{DisposableDelegate:()=>p,DisposableSet:()=>c,ObservableDisposableDelegate:()=>u,ObservableDisposableSet:()=>a});var o=i(44878),n=i(70525),s=function(t,e){return s=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])},s(t,e)};function r(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function i(){this.constructor=t}s(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}var p=function(){function t(t){this._fn=t}return Object.defineProperty(t.prototype,"isDisposed",{get:function(){return!this._fn},enumerable:!0,configurable:!0}),t.prototype.dispose=function(){if(this._fn){var t=this._fn;this._fn=null,t()}},t}(),u=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e._disposed=new n.Signal(e),e}return r(e,t),Object.defineProperty(e.prototype,"disposed",{get:function(){return this._disposed},enumerable:!0,configurable:!0}),e.prototype.dispose=function(){this.isDisposed||(t.prototype.dispose.call(this),this._disposed.emit(void 0),n.Signal.clearData(this))},e}(p),c=function(){function t(){this._isDisposed=!1,this._items=new Set}return Object.defineProperty(t.prototype,"isDisposed",{get:function(){return this._isDisposed},enumerable:!0,configurable:!0}),t.prototype.dispose=function(){this._isDisposed||(this._isDisposed=!0,this._items.forEach((function(t){t.dispose()})),this._items.clear())},t.prototype.contains=function(t){return this._items.has(t)},t.prototype.add=function(t){this._items.add(t)},t.prototype.remove=function(t){this._items.delete(t)},t.prototype.clear=function(){this._items.clear()},t}();!function(t){t.from=function(e){var i=new t;return(0,o.each)(e,(function(t){i.add(t)})),i}}(c||(c={}));var a=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e._disposed=new n.Signal(e),e}return r(e,t),Object.defineProperty(e.prototype,"disposed",{get:function(){return this._disposed},enumerable:!0,configurable:!0}),e.prototype.dispose=function(){this.isDisposed||(t.prototype.dispose.call(this),this._disposed.emit(void 0),n.Signal.clearData(this))},e}(c);!function(t){t.from=function(e){var i=new t;return(0,o.each)(e,(function(t){i.add(t)})),i}}(a||(a={}))}}]);