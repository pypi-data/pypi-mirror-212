import { JupyterCadModel } from '../model';
/**
 * A Model factory to create new instances of JupyterCadModel.
 */
export class JupyterCadFCModelFactory {
    constructor(options) {
        /**
         * Whether the model is collaborative or not.
         */
        this.collaborative = true;
        this._disposed = false;
        this._annotationModel = options.annotationModel;
    }
    /**
     * The name of the model.
     *
     * @returns The name
     */
    get name() {
        return 'jupytercad-fcmodel';
    }
    /**
     * The content type of the file.
     *
     * @returns The content type
     */
    get contentType() {
        return 'FCStd';
    }
    /**
     * The format of the file.
     *
     * @returns the file format
     */
    get fileFormat() {
        return 'base64';
    }
    /**
     * Get whether the model factory has been disposed.
     *
     * @returns disposed status
     */
    get isDisposed() {
        return this._disposed;
    }
    /**
     * Dispose the model factory.
     */
    dispose() {
        this._disposed = true;
    }
    /**
     * Get the preferred language given the path on the file.
     *
     * @param path path of the file represented by this document model
     * @returns The preferred language
     */
    preferredLanguage(path) {
        return '';
    }
    /**
     * Create a new instance of JupyterCadModel.
     *
     * @returns The model
     */
    createNew(options) {
        const model = new JupyterCadModel({
            sharedModel: options.sharedModel,
            languagePreference: options.languagePreference,
            annotationModel: this._annotationModel
        });
        return model;
    }
}
