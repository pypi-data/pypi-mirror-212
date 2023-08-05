import { TopoDS_Shape } from '@jupytercad/jupytercad-opencascade';
import { IJCadContent, Parts } from '../_interface/jcad';
import { IDict } from '../types';
export declare function expand_operator(name: Parts | 'BrepFile', args: any, content: IJCadContent): IDict;
export declare function operatorCache<T>(name: Parts | 'BrepFile', ops: (args: T, content: IJCadContent) => TopoDS_Shape | undefined): (args: T, content: IJCadContent) => TopoDS_Shape | undefined;
