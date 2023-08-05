/* tslint:disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

/**
 * Part::MultiFuse
 */
export interface IFuse {
  /**
   * The shapes of the individual elements
   */
  Shapes: string[];
  /**
   * Refine shape
   */
  Refine: boolean;
  /**
   * Placement of the box
   */
  Placement: {
    /**
     * Position of the Placement
     */
    Position: number[];
    /**
     * Axis of the Placement
     */
    Axis: number[];
    /**
     * Angle of the Placement
     */
    Angle: number;
  };
}
