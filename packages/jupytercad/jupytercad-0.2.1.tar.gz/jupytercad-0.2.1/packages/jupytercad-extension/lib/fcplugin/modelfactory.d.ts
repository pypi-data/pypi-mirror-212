import { DocumentRegistry } from '@jupyterlab/docregistry';
import { Contents } from '@jupyterlab/services';
import { IAnnotationModel, IJupyterCadDoc } from '../types';
import { JupyterCadModel } from '../model';
/**
 * A Model factory to create new instances of JupyterCadModel.
 */
export declare class JupyterCadFCModelFactory implements DocumentRegistry.IModelFactory<JupyterCadModel> {
    constructor(options: JupyterCadFCModelFactory.IOptions);
    /**
     * Whether the model is collaborative or not.
     */
    readonly collaborative = true;
    /**
     * The name of the model.
     *
     * @returns The name
     */
    get name(): string;
    /**
     * The content type of the file.
     *
     * @returns The content type
     */
    get contentType(): Contents.ContentType;
    /**
     * The format of the file.
     *
     * @returns the file format
     */
    get fileFormat(): Contents.FileFormat;
    /**
     * Get whether the model factory has been disposed.
     *
     * @returns disposed status
     */
    get isDisposed(): boolean;
    /**
     * Dispose the model factory.
     */
    dispose(): void;
    /**
     * Get the preferred language given the path on the file.
     *
     * @param path path of the file represented by this document model
     * @returns The preferred language
     */
    preferredLanguage(path: string): string;
    /**
     * Create a new instance of JupyterCadModel.
     *
     * @returns The model
     */
    createNew(options: DocumentRegistry.IModelOptions<IJupyterCadDoc>): JupyterCadModel;
    private _annotationModel;
    private _disposed;
}
export declare namespace JupyterCadFCModelFactory {
    interface IOptions {
        annotationModel: IAnnotationModel;
    }
}
