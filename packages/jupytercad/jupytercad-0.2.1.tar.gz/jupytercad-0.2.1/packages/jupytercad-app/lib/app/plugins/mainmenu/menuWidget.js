import { RankedMenu, MenuSvg, homeIcon } from '@jupyterlab/ui-components';
import { MenuBar } from '@lumino/widgets';
import { CommandIDs } from '@jupytercad/jupytercad-extension/lib/commands';
export class MainMenu extends MenuBar {
    constructor(options) {
        super({ forceItemsPosition: { forceX: false, forceY: true } });
        this._commands = options.commands;
        this._themeManager = options.themeManager;
        this.addClass('jc-MainMenu');
        this._createFileMenu();
        this._createEditMenu();
        this._createViewMenu();
        this._createHelpMenu();
    }
    _createHelpMenu() {
        this._commands.addCommand('jupytercad:help-menu:documentation', {
            label: 'Documentation',
            execute: () => {
                window.open('https://github.com/QuantStack/jupytercad', '_blank');
            },
            icon: homeIcon
        });
        const helpMenu = new MenuSvg({
            commands: this._commands
        });
        helpMenu.title.label = 'Help';
        helpMenu.title.mnemonic = 0;
        helpMenu.addClass('jc-MenuBar-MenuItem');
        this.addMenu(helpMenu);
        helpMenu.addItem({
            type: 'command',
            command: 'jupytercad:help-menu:documentation'
        });
    }
    _createFileMenu() {
        const menu = new MenuSvg({
            commands: this._commands
        });
        menu.title.label = 'File';
        menu.title.mnemonic = 0;
        menu.addClass('jc-MenuBar-FileMenu');
        menu.addClass('jc-MenuBar-MenuItem');
        this.addMenu(menu);
        menu.addItem({
            type: 'command',
            command: 'jupytercad:create-new-jcad-file'
        });
        menu.addItem({
            type: 'command',
            command: 'jupytercad:open-file'
        });
    }
    _createEditMenu() {
        const menu = new MenuSvg({
            commands: this._commands
        });
        menu.title.label = 'Edit';
        menu.title.mnemonic = 0;
        menu.addClass('jc-MenuBar-MenuItem');
        this.addMenu(menu);
        const shapeMenu = new RankedMenu({
            commands: this._commands,
            rank: 200
        });
        shapeMenu.title.label = 'Shape';
        shapeMenu.addClass('jc-MenuBar-MenuItem');
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newBox
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newCone
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newCylinder
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newSketch
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newSphere
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newTorus
        });
        shapeMenu.addItem({
            type: 'command',
            command: CommandIDs.newCone
        });
        menu.addItem({
            type: 'submenu',
            submenu: shapeMenu
        });
        const operatorMenu = new RankedMenu({
            commands: this._commands,
            rank: 200
        });
        operatorMenu.title.label = 'Operators';
        operatorMenu.addClass('jc-MenuBar-MenuItem');
        operatorMenu.addItem({
            type: 'command',
            command: CommandIDs.cut
        });
        operatorMenu.addItem({
            type: 'command',
            command: CommandIDs.extrusion
        });
        operatorMenu.addItem({
            type: 'command',
            command: CommandIDs.intersection
        });
        operatorMenu.addItem({
            type: 'command',
            command: CommandIDs.union
        });
        menu.addItem({
            type: 'submenu',
            submenu: operatorMenu
        });
        menu.addItem({
            type: 'command',
            command: CommandIDs.undo
        });
        menu.addItem({
            type: 'command',
            command: CommandIDs.redo
        });
    }
    _createViewMenu() {
        const menu = new MenuSvg({
            commands: this._commands
        });
        menu.title.label = 'View';
        menu.title.mnemonic = 0;
        menu.addClass('jc-MenuBar-ViewMenu');
        menu.addClass('jc-MenuBar-MenuItem');
        this.addMenu(menu);
        menu.addItem({
            type: 'command',
            command: CommandIDs.updateExplodedView
        });
        menu.addItem({
            type: 'command',
            command: CommandIDs.updateAxes
        });
        const themeMenu = new RankedMenu({
            commands: this._commands,
            rank: 200
        });
        themeMenu.title.label = 'Theme';
        themeMenu.addClass('jc-MenuBar-MenuItem');
        this._themeManager.themes.forEach((theme, index) => {
            themeMenu.insertItem(index, {
                command: 'apputils:change-theme',
                args: { theme }
            });
        });
        menu.addItem({
            type: 'submenu',
            submenu: themeMenu
        });
    }
}
