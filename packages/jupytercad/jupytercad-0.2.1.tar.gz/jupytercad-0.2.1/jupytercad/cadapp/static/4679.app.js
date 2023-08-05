"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[4679,2970],{34679:(e,t,o)=>{o.r(t),o.d(t,{default:()=>P,fileUploadStatus:()=>k});var r=o(41508),n=o(45494),a=o(55455),i=o(43827),s=o(91139),l=o(23358),d=o(4133),c=o(22970),u=o(77352),m=o(42122),h=o(18246),p=o(1745);const w="FileBrowser",f="@jupyterlab/filebrowser-extension:browser";var g;!function(e){e.copy="filebrowser:copy",e.copyDownloadLink="filebrowser:copy-download-link",e.cut="filebrowser:cut",e.del="filebrowser:delete",e.download="filebrowser:download",e.duplicate="filebrowser:duplicate",e.hideBrowser="filebrowser:hide-main",e.goToPath="filebrowser:go-to-path",e.goUp="filebrowser:go-up",e.openPath="filebrowser:open-path",e.openUrl="filebrowser:open-url",e.open="filebrowser:open",e.openBrowserTab="filebrowser:open-browser-tab",e.paste="filebrowser:paste",e.createNewDirectory="filebrowser:create-new-directory",e.createNewFile="filebrowser:create-new-file",e.createNewMarkdownFile="filebrowser:create-new-markdown-file",e.refresh="filebrowser:refresh",e.rename="filebrowser:rename",e.copyShareableLink="filebrowser:share-main",e.copyPath="filebrowser:copy-path",e.showBrowser="filebrowser:activate",e.shutdown="filebrowser:shutdown",e.toggleBrowser="filebrowser:toggle-main",e.toggleNavigateToCurrentDirectory="filebrowser:toggle-navigate-to-current-directory",e.toggleLastModified="filebrowser:toggle-last-modified",e.toggleFileSize="filebrowser:toggle-file-size",e.search="filebrowser:search",e.toggleHiddenFiles="filebrowser:toggle-hidden-files",e.toggleFileCheckboxes="filebrowser:toggle-file-checkboxes"}(g||(g={}));const b="filebrowser",y={id:f,description:"Set up the default file browser (commands, settings,...).",requires:[s.IDefaultFileBrowser,s.IFileBrowserFactory,u.ITranslator],optional:[r.ILayoutRestorer,l.ISettingRegistry,r.ITreePathUpdater,n.ICommandPalette],provides:s.IFileBrowserCommands,autoStart:!0,activate:async(e,t,o,r,i,s,l,d)=>{const c=t;i&&i.add(c,b);const u=a.PageConfig.getOption("preferredPath");u&&await c.model.cd(u),function(e,t,o,r,i,s){const l=r.load("jupyterlab"),{docRegistry:d,commands:c}=e,{tracker:u}=o;c.addCommand(g.del,{execute:()=>{const e=u.currentWidget;if(e)return e.delete()},icon:m.closeIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Delete"),mnemonic:0}),c.addCommand(g.copy,{execute:()=>{const e=u.currentWidget;if(e)return e.copy()},icon:m.copyIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Copy"),mnemonic:0}),c.addCommand(g.cut,{execute:()=>{const e=u.currentWidget;if(e)return e.cut()},icon:m.cutIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Cut")}),c.addCommand(g.duplicate,{execute:()=>{const e=u.currentWidget;if(e)return e.duplicate()},icon:m.copyIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Duplicate")}),c.addCommand(g.goToPath,{label:l.__("Update the file browser to display the provided `path`."),execute:async e=>{var n;const a=e.path||"",i=!(null!==(n=null==e?void 0:e.dontShowBrowser)&&void 0!==n&&n);try{if("directory"!==(await T.navigateToPath(a,t,o,r)).type&&i){const e=T.getBrowserForPath(a,t,o);if(e){e.clearSelectedItems();const t=a.split("/"),o=t[t.length-1];o&&await e.selectItemByName(o)}}}catch(e){console.warn(`${g.goToPath} failed to go to: ${a}`,e)}if(i)return c.execute(g.showBrowser,{path:a})}}),c.addCommand(g.goUp,{label:"go up",execute:async()=>{const e=T.getBrowserForPath("",t,o);if(!e)return;const{model:r}=e;await r.restored,e.goUp()}}),c.addCommand(g.openPath,{label:e=>e.path?l.__("Open %1",e.path):l.__("Open from Path…"),caption:e=>e.path?l.__("Open %1",e.path):l.__("Open from path"),execute:async e=>{var r;let a;if(a=(null==e?void 0:e.path)?e.path:null!==(r=(await n.InputDialog.getText({label:l.__("Path"),placeholder:"/path/relative/to/jlab/root",title:l.__("Open Path"),okLabel:l.__("Open")})).value)&&void 0!==r?r:void 0,a)try{const r="/"!==a&&a.endsWith("/");r&&(a=a.slice(0,a.length-1));const n=T.getBrowserForPath(a,t,o),{services:i}=n.model.manager,s=await i.contents.get(a,{content:!1});if(r&&"directory"!==s.type)throw new Error(`Path ${a}/ is not a directory`);if(await c.execute(g.goToPath,{path:a,dontShowBrowser:e.dontShowBrowser}),"directory"===s.type)return;return c.execute("docmanager:open",{path:a})}catch(e){return e.response&&404===e.response.status&&(e.message=l.__("Could not find path: %1",a)),(0,n.showErrorMessage)(l.__("Cannot open"),e)}}}),s&&s.addItem({command:g.openPath,category:l.__("File Operations")}),c.addCommand(g.open,{execute:e=>{const t=e.factory||void 0,o=u.currentWidget;if(!o)return;const{contents:r}=o.model.manager.services;return Promise.all(Array.from((0,h.map)(o.selectedItems(),(e=>{if("directory"===e.type){const t=r.localPath(e.path);return o.model.cd(`/${t}`)}return c.execute("docmanager:open",{factory:t,path:e.path})}))))},icon:e=>{var t;const o=e.factory||void 0;if(o){const e=d.getFileType(o);return null===(t=null==e?void 0:e.icon)||void 0===t?void 0:t.bindprops({stylesheet:"menuItem"})}return m.folderIcon.bindprops({stylesheet:"menuItem"})},label:e=>e.label||e.factory||l.__("Open"),mnemonic:0}),c.addCommand(g.paste,{execute:()=>{const e=u.currentWidget;if(e)return e.paste()},icon:m.pasteIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Paste"),mnemonic:0}),c.addCommand(g.createNewDirectory,{execute:()=>{const e=u.currentWidget;if(e)return e.createNewDirectory()},icon:m.newFolderIcon.bindprops({stylesheet:"menuItem"}),label:l.__("New Folder")}),c.addCommand(g.createNewFile,{execute:()=>{const e=u.currentWidget;if(e)return e.createNewFile({ext:"txt"})},icon:m.textEditorIcon.bindprops({stylesheet:"menuItem"}),label:l.__("New File")}),c.addCommand(g.createNewMarkdownFile,{execute:()=>{const e=u.currentWidget;if(e)return e.createNewFile({ext:"md"})},icon:m.markdownIcon.bindprops({stylesheet:"menuItem"}),label:l.__("New Markdown File")}),c.addCommand(g.refresh,{execute:e=>{const t=u.currentWidget;if(t)return t.model.refresh()},icon:m.refreshIcon.bindprops({stylesheet:"menuItem"}),caption:l.__("Refresh the file browser."),label:l.__("Refresh File List")}),c.addCommand(g.rename,{execute:e=>{const t=u.currentWidget;if(t)return t.rename()},isVisible:()=>!!u.currentWidget&&1===Array.from(u.currentWidget.selectedItems()).length,icon:m.editIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Rename"),mnemonic:0}),c.addCommand(g.copyPath,{execute:()=>{const e=u.currentWidget;if(!e)return;const t=e.selectedItems().next();t.done||n.Clipboard.copyToSystem(t.value.path)},isVisible:()=>!!u.currentWidget&&1===Array.from(u.currentWidget.selectedItems()).length,icon:m.fileIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Copy Path")}),c.addCommand(g.shutdown,{execute:()=>{const e=u.currentWidget;if(e)return e.shutdownKernels()},icon:m.stopIcon.bindprops({stylesheet:"menuItem"}),label:l.__("Shut Down Kernel")}),c.addCommand(g.toggleLastModified,{label:l.__("Show Last Modified Column"),isToggled:()=>t.showLastModifiedColumn,execute:()=>{const e=!t.showLastModifiedColumn,o="showLastModifiedColumn";if(i)return i.set(f,o,e).catch((e=>{console.error(`Failed to set ${o} setting`)}))}}),c.addCommand(g.toggleFileSize,{label:l.__("Show File Size Column"),isToggled:()=>t.showFileSizeColumn,execute:()=>{const e=!t.showFileSizeColumn,o="showFileSizeColumn";if(i)return i.set(f,o,e).catch((e=>{console.error(`Failed to set ${o} setting`)}))}}),c.addCommand(g.toggleHiddenFiles,{label:l.__("Show Hidden Files"),isToggled:()=>t.showHiddenFiles,isVisible:()=>"true"===a.PageConfig.getOption("allow_hidden_files"),execute:()=>{const e=!t.showHiddenFiles;if(i)return i.set(f,"showHiddenFiles",e).catch((e=>{console.error("Failed to set showHiddenFiles setting")}))}}),c.addCommand(g.toggleFileCheckboxes,{label:l.__("Show File Checkboxes"),isToggled:()=>t.showFileCheckboxes,execute:()=>{const e=!t.showFileCheckboxes;if(i)return i.set(f,"showFileCheckboxes",e).catch((e=>{console.error("Failed to set showFileCheckboxes setting")}))}}),c.addCommand(g.search,{label:l.__("Search on File Names"),execute:()=>alert("search")})}(e,c,o,r,s,d),Promise.all([e.restored,c.model.restored]).then((()=>{l&&c.model.pathChanged.connect(((e,t)=>{l(t.newValue)})),s&&s.load(f).then((e=>{const t={navigateToCurrentDirectory:!1,showLastModifiedColumn:!0,showFileSizeColumn:!1,showHiddenFiles:!1,showFileCheckboxes:!1},o={filterDirectories:!0};function r(e){let r;for(r in t){const o=e.get(r).composite;t[r]=o,c[r]=o}const n=e.get("filterDirectories").composite;o.filterDirectories=n,c.model.filterDirectories=n}e.changed.connect(r),r(e)}))}))}},v={id:"@jupyterlab/filebrowser-extension:factory",description:"Provides the file browser factory.",provides:s.IFileBrowserFactory,requires:[i.IDocumentManager,u.ITranslator],optional:[d.IStateDB,r.JupyterLab.IInfo],activate:async(e,t,o,r,a)=>{const i=new n.WidgetTracker({namespace:b});return{createFileBrowser:(e,n={})=>{var l;const d=new s.FilterFileBrowserModel({translator:o,auto:null===(l=n.auto)||void 0===l||l,manager:t,driveName:n.driveName||"",refreshInterval:n.refreshInterval,refreshStandby:()=>a&&!a.isConnected||"when-hidden",state:null===n.state?void 0:n.state||r||void 0}),c=n.restore,u=new s.FileBrowser({id:e,model:d,restore:c,translator:o});return i.add(u),u},tracker:i}}},_={id:"@jupyterlab/filebrowser-extension:default-file-browser",description:"Provides the default file browser",provides:s.IDefaultFileBrowser,requires:[s.IFileBrowserFactory],optional:[r.IRouter,r.JupyterFrontEnd.ITreeResolver,r.ILabShell],activate:async(e,t,o,r,n)=>{const{commands:a}=e,i=t.createFileBrowser("filebrowser",{auto:!1,restore:!1});return T.restoreBrowser(i,a,o,r,e,n),i}},C={id:"@jupyterlab/filebrowser-extension:download",description:"Adds the download file commands. Disabling this plugin will NOT disable downloading files from the server, if the user enters the appropriate download URLs.",requires:[s.IFileBrowserFactory,u.ITranslator],autoStart:!0,activate:(e,t,o)=>{const r=o.load("jupyterlab"),{commands:a}=e,{tracker:i}=t;a.addCommand(g.download,{execute:()=>{const e=i.currentWidget;if(e)return e.download()},icon:m.downloadIcon.bindprops({stylesheet:"menuItem"}),label:r.__("Download")}),a.addCommand(g.copyDownloadLink,{execute:()=>{const e=i.currentWidget;if(e)return e.model.manager.services.contents.getDownloadUrl(e.selectedItems().next().value.path).then((e=>{n.Clipboard.copyToSystem(e)}))},isVisible:()=>!!i.currentWidget&&1===Array.from(i.currentWidget.selectedItems()).length,icon:m.copyIcon.bindprops({stylesheet:"menuItem"}),label:r.__("Copy Download Link"),mnemonic:0})}},F={id:"@jupyterlab/filebrowser-extension:widget",description:"Adds the file browser to the application shell.",requires:[i.IDocumentManager,s.IDefaultFileBrowser,s.IFileBrowserFactory,l.ISettingRegistry,n.IToolbarWidgetRegistry,u.ITranslator,r.ILabShell,s.IFileBrowserCommands],optional:[n.ICommandPalette],autoStart:!0,activate:(e,t,o,r,a,i,l,d,c,u)=>{const{commands:b}=e,{tracker:y}=r,v=l.load("jupyterlab");o.node.setAttribute("role","region"),o.node.setAttribute("aria-label",v.__("File Browser Section")),o.title.icon=m.folderIcon;const _=()=>{const t=(0,h.find)(e.commands.keyBindings,(e=>e.command===g.toggleBrowser));if(t){const e=t.keys.map(p.CommandRegistry.formatKeystroke).join(", ");o.title.caption=v.__("File Browser (%1)",e)}else o.title.caption=v.__("File Browser")};_(),e.commands.keyBindingChanged.connect((()=>{_()})),i.addFactory(w,"uploader",(e=>new s.Uploader({model:e.model,translator:l}))),i.addFactory(w,"fileNameSearcher",(e=>{const t=(0,m.FilenameSearcher)({updateFilter:(t,o)=>{e.model.setFilter((e=>t(e.name.toLowerCase())))},useFuzzyFilter:!0,placeholder:v.__("Filter files by name"),forceRefresh:!0});return t.addClass("jp-FileBrowser-filterBox"),t})),(0,n.setToolbar)(o,(0,n.createToolbarFactory)(i,a,w,F.id,l)),d.add(o,"left",{rank:100,type:"File Browser"}),b.addCommand(g.toggleBrowser,{label:v.__("File Browser"),execute:()=>o.isHidden?b.execute(g.showBrowser,void 0):b.execute(g.hideBrowser,void 0)}),b.addCommand(g.showBrowser,{label:v.__("Open the file browser for the provided `path`."),execute:e=>{const t=e.path||"",n=T.getBrowserForPath(t,o,r);if(n)if(o!==n){const e=["left","right"];for(const t of e)for(const e of d.widgets(t))if(e.contains(n))return void d.activateById(e.id)}else d.activateById(o.id)}}),b.addCommand(g.hideBrowser,{label:v.__("Hide the file browser."),execute:()=>{const e=y.currentWidget;e&&!e.isHidden&&d.collapseLeft()}}),b.addCommand(g.toggleNavigateToCurrentDirectory,{label:v.__("Show Active File in File Browser"),isToggled:()=>o.navigateToCurrentDirectory,execute:()=>{const e=!o.navigateToCurrentDirectory;return a.set(f,"navigateToCurrentDirectory",e).catch((e=>{console.error("Failed to set navigateToCurrentDirectory setting")}))}}),u&&u.addItem({command:g.toggleNavigateToCurrentDirectory,category:v.__("File Operations")}),d.restored.then((e=>{e.fresh&&"single-document"!==d.mode&&b.execute(g.showBrowser,void 0)})),Promise.all([e.restored,o.model.restored]).then((()=>{d.currentChanged.connect((async(e,n)=>{if(o.navigateToCurrentDirectory&&n.newValue){const{newValue:e}=n,a=t.contextForWidget(e);if(a){const{path:e}=a;try{await T.navigateToPath(e,o,r,l)}catch(t){console.warn(`${g.goToPath} failed to open: ${e}`,t)}}}}))}))}},I={id:"@jupyterlab/filebrowser-extension:share-file",description:'Adds the "Copy Shareable Link" command; useful for JupyterHub deployment for example.',requires:[s.IFileBrowserFactory,u.ITranslator],autoStart:!0,activate:(e,t,o)=>{const r=o.load("jupyterlab"),{commands:i}=e,{tracker:s}=t;i.addCommand(g.copyShareableLink,{execute:()=>{const e=s.currentWidget,t=null==e?void 0:e.selectedItems().next();void 0===t||t.done||n.Clipboard.copyToSystem(a.PageConfig.getUrl({workspace:a.PageConfig.defaultWorkspace,treePath:t.value.path,toShare:!0}))},isVisible:()=>!!s.currentWidget&&1===Array.from(s.currentWidget.selectedItems()).length,icon:m.linkIcon.bindprops({stylesheet:"menuItem"}),label:r.__("Copy Shareable Link")})}},x={id:"@jupyterlab/filebrowser-extension:open-with",description:"Adds the open-with feature allowing an user to pick the non-preferred document viewer.",requires:[s.IFileBrowserFactory],autoStart:!0,activate:(e,t)=>{const{docRegistry:o}=e,{tracker:r}=t;let n=[];e.contextMenu.opened.connect((function(e){var t,a;const i=null!==(a=null===(t=e.menu.items.find((e=>{var t;return"submenu"===e.type&&"jp-contextmenu-open-with"===(null===(t=e.submenu)||void 0===t?void 0:t.id)})))||void 0===t?void 0:t.submenu)&&void 0!==a?a:null;if(!i)return;n.forEach((e=>e.dispose())),n.length=0,i.clearItems();const s=r.currentWidget?T.OpenWith.intersection((0,h.map)(r.currentWidget.selectedItems(),(e=>T.OpenWith.getFactories(o,e)))):new Set;n=[...s].map((e=>i.addItem({args:{factory:e.name,label:e.label||e.name},command:g.open})))}))}},B={id:"@jupyterlab/filebrowser-extension:open-browser-tab",description:"Adds the open-in-new-browser-tab features.",requires:[s.IFileBrowserFactory,u.ITranslator],autoStart:!0,activate:(e,t,o)=>{const{commands:r}=e,n=o.load("jupyterlab"),{tracker:i}=t;r.addCommand(g.openBrowserTab,{execute:e=>{const t=i.currentWidget;if(!t)return;const o=e.mode;return Promise.all(Array.from((0,h.map)(t.selectedItems(),(e=>{if("single-document"!==o)return r.execute("docmanager:open-browser-tab",{path:e.path});{const t=a.PageConfig.getUrl({mode:"single-document",treePath:e.path}),o=window.open();if(!o)throw new Error("Failed to open new browser tab.");o.opener=null,o.location.href=t}}))))},icon:m.addIcon.bindprops({stylesheet:"menuItem"}),label:e=>"single-document"===e.mode?n.__("Open in Simple Mode"):n.__("Open in New Browser Tab"),mnemonic:0})}},k={id:"@jupyterlab/filebrowser-extension:file-upload-status",description:"Adds a file upload status widget.",autoStart:!0,requires:[s.IFileBrowserFactory,u.ITranslator],optional:[c.WQ],activate:(e,t,o,r)=>{if(!r)return;const n=new s.FileUploadStatus({tracker:t.tracker,translator:o});r.registerStatusItem("@jupyterlab/filebrowser-extension:file-upload-status",{item:n,align:"middle",isActive:()=>!!n.model&&n.model.items.length>0,activeStateChanged:n.model.stateChanged})}},S={id:"@jupyterlab/filebrowser-extension:open-url",description:'Adds the feature "Open files from remote URLs".',autoStart:!0,requires:[s.IDefaultFileBrowser,u.ITranslator],optional:[n.ICommandPalette],activate:(e,t,o,r)=>{const{commands:i}=e,s=o.load("jupyterlab"),l=g.openUrl;i.addCommand(l,{label:e=>e.url?s.__("Open %1",e.url):s.__("Open from URL…"),caption:e=>e.url?s.__("Open %1",e.url):s.__("Open from URL"),execute:async e=>{var o,r,l;let d=null!==(o=null==e?void 0:e.url)&&void 0!==o?o:"";if(d||(d=null!==(r=(await n.InputDialog.getText({label:s.__("URL"),placeholder:"https://example.com/path/to/file",title:s.__("Open URL"),okLabel:s.__("Open")})).value)&&void 0!==r?r:void 0),!d)return;let c,u="";try{const e=await fetch(d);c=await e.blob(),u=null!==(l=e.headers.get("Content-Type"))&&void 0!==l?l:""}catch(e){return e.response&&200!==e.response.status&&(e.message=s.__("Could not open URL: %1",d)),(0,n.showErrorMessage)(s.__("Cannot fetch"),e)}try{const e=a.PathExt.basename(d),o=new File([c],e,{type:u}),r=await t.model.upload(o);return i.execute("docmanager:open",{path:r.path})}catch(e){return(0,n.showErrorMessage)(s._p("showErrorMessage","Upload Error"),e)}}}),r&&r.addItem({command:l,category:s.__("File Operations")})}},P=[v,_,y,I,k,C,F,x,B,S];var T;!function(e){let t;e.getBrowserForPath=function(e,t,o){const{tracker:r}=o,n=t.model.manager.services.contents.driveName(e);if(n){return r.find((e=>e.model.driveName===n))||void console.warn(`${g.goToPath} failed to find filebrowser for path: ${e}`)}return t},e.navigateToPath=async function(t,o,r,n){const i=n.load("jupyterlab"),s=e.getBrowserForPath(t,o,r);if(!s)throw new Error(i.__("No browser for path"));const{services:l}=s.model.manager,d=l.contents.localPath(t);await l.ready;const c=await l.contents.get(t,{content:!1}),{model:u}=s;return await u.restored,"directory"===c.type?await u.cd(`/${d}`):await u.cd(`/${a.PathExt.dirname(d)}`),c},e.restoreBrowser=async function(e,t,o,r,n,a){const i="jp-mod-restoring";if(e.addClass(i),!o)return await e.model.restore(e.id),await e.model.refresh(),void e.removeClass(i);const s=async()=>{o.routed.disconnect(s);const n=await(null==r?void 0:r.paths);(null==n?void 0:n.file)||(null==n?void 0:n.browser)?(await e.model.restore(e.id,!1),n.file&&await t.execute(g.openPath,{path:n.file,dontShowBrowser:!0}),n.browser&&await t.execute(g.openPath,{path:n.browser,dontShowBrowser:!0})):(await e.model.restore(e.id),await e.model.refresh()),e.removeClass(i),(null==a?void 0:a.isEmpty("main"))&&t.execute("launcher:create")};o.routed.connect(s)},function(e){e.getFactories=function(e,t){const o=e.preferredWidgetFactories(t.path),r=e.getWidgetFactory("notebook");return r&&"notebook"===t.type&&-1===o.indexOf(r)&&o.unshift(r),o},e.intersection=function(e){let t;for(const o of e){if(void 0===t){t=new Set(o);continue}if(0===t.size)return t;let e=new Set;for(const r of o)t.has(r)&&e.add(r);t=e}return null!=t?t:new Set}}(t=e.OpenWith||(e.OpenWith={}))}(T||(T={}))},22970:(e,t,o)=>{o.d(t,{MN:()=>a,WQ:()=>w,ko:()=>u,_3:()=>p,Jy:()=>h,U:()=>d});var r=o(93119),n=o.n(r);function a(e){const{spacing:t,children:o,className:n,...a}=e,i=r.Children.count(o);return r.createElement("div",{className:`jp-StatusBar-GroupItem ${n||""}`,...a},r.Children.map(o,((e,o)=>0===o?r.createElement("div",{style:{marginRight:`${t}px`}},e):o===i-1?r.createElement("div",{style:{marginLeft:`${t}px`}},e):r.createElement("div",{style:{margin:`0px ${t}px`}},e))))}var i,s=o(42122),l=o(23190);function d(e){const t=new c(e);return e.startHidden||t.launch(),t}class c extends l.Widget{constructor(e){super(),this._body=e.body,this._body.addClass("jp-StatusBar-HoverItem"),this._anchor=e.anchor,this._align=e.align,e.hasDynamicSize&&(this._observer=new ResizeObserver((()=>{this.update()}))),(this.layout=new l.PanelLayout).addWidget(e.body),this._body.node.addEventListener("resize",(()=>{this.update()}))}launch(){this._setGeometry(),l.Widget.attach(this,document.body),this.update(),this._anchor.addClass("jp-mod-clicked"),this._anchor.removeClass("jp-mod-highlight")}onUpdateRequest(e){this._setGeometry(),super.onUpdateRequest(e)}onAfterAttach(e){var t;document.addEventListener("click",this,!1),this.node.addEventListener("keydown",this,!1),window.addEventListener("resize",this,!1),null===(t=this._observer)||void 0===t||t.observe(this._body.node)}onBeforeDetach(e){var t;null===(t=this._observer)||void 0===t||t.disconnect(),document.removeEventListener("click",this,!1),this.node.removeEventListener("keydown",this,!1),window.removeEventListener("resize",this,!1)}onResize(){this.update()}dispose(){var e;null===(e=this._observer)||void 0===e||e.disconnect(),super.dispose(),this._anchor.removeClass("jp-mod-clicked"),this._anchor.addClass("jp-mod-highlight")}handleEvent(e){switch(e.type){case"keydown":this._evtKeydown(e);break;case"click":this._evtClick(e);break;case"resize":this.onResize()}}_evtClick(e){!e.target||this._body.node.contains(e.target)||this._anchor.node.contains(e.target)||this.dispose()}_evtKeydown(e){27===e.keyCode&&(e.stopPropagation(),e.preventDefault(),this.dispose())}_setGeometry(){let e=0;const t=this._anchor.node.getBoundingClientRect(),o=this._body.node.getBoundingClientRect();"right"===this._align&&(e=-(o.width-t.width));const r=window.getComputedStyle(this._body.node);s.HoverBox.setGeometry({anchor:t,host:document.body,maxHeight:500,minHeight:20,node:this._body.node,offset:{horizontal:e},privilege:"forceAbove",style:r})}}function u(e){const{width:t,percentage:o,...n}=e;return r.createElement("div",{className:"jp-Statusbar-ProgressBar-progress-bar",role:"progressbar","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":o},r.createElement(m,{...{percentage:o,...n},contentWidth:t}))}function m(e){return r.createElement("div",{style:{width:`${e.percentage}%`}},r.createElement("p",null,e.content))}function h(e){const{title:t,source:o,className:n,...a}=e;return r.createElement("span",{className:`jp-StatusBar-TextItem ${n}`,title:t,...a},o)}function p(e){return n().createElement("div",{className:"jp-Statusbar-ProgressCircle",role:"progressbar","aria-label":e.label||"Unlabelled progress circle","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":e.progress},n().createElement("svg",{viewBox:"0 0 250 250"},n().createElement("circle",{cx:"125",cy:"125",r:"104",stroke:"var(--jp-inverse-layout-color3)",strokeWidth:"20",fill:"none"}),n().createElement("path",{transform:"translate(125,125) scale(.9)",d:(e=>{const t=Math.max(3.6*e,.1),o=t*Math.PI/180,r=104*Math.sin(o),n=-104*Math.cos(o);return"M 0 0 v -104 A 104 104 1 "+(t<180?1:0)+" 0 "+r.toFixed(4)+" "+n.toFixed(4)+" z"})(e.progress),fill:"var(--jp-inverse-layout-color3)"})))}o(18246),o(75324),function(e){e.statusItemDefaults={align:"left",rank:0,isActive:()=>!0,activeStateChanged:void 0}}(i||(i={}));const w=new(o(50558).Token)("@jupyterlab/statusbar:IStatusBar","A service for the status bar on the application. Use this if you want to add new status bar items.")}}]);