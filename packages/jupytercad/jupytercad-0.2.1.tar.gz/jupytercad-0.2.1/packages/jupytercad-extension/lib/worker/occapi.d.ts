import { TopoDS_Shape } from '@jupytercad/jupytercad-opencascade';
import { IJCadContent, Parts } from '../_interface/jcad';
import { ISketchObject } from '../_interface/sketch';
import { IAllOperatorFunc } from './types';
export declare function _SketchObject(arg: ISketchObject, content: IJCadContent): TopoDS_Shape | undefined;
export declare function _loadBrep(arg: {
    content: string;
}): TopoDS_Shape | undefined;
export declare const BrepFile: (args: {
    content: string;
}, content: IJCadContent) => TopoDS_Shape | undefined;
export declare const ShapesFactory: {
    [key in Parts]: IAllOperatorFunc;
};
