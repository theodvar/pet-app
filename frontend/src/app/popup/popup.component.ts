import { Component, Input, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';
import { PetPointOfInterestService } from '../services/petpointofinterest.service';
import { DogParksService } from '../services/dogparks.service';
import { DogWalksService } from '../services/dogwalks.service';
import { Feature } from 'ol';
import { FormsModule } from '@angular/forms';
import GeoJSON from 'ol/format/GeoJSON';
import { fromLonLat, toLonLat } from 'ol/proj';


@Component({
  selector: 'app-popup',
  imports: [CommonModule,
    FormsModule],
  templateUrl: './popup.component.html',
  styleUrl: './popup.component.css'
})
export class PopupComponent {

  @Input() data: any;
  @Input() position: number[] | undefined;
  @Input() feature!: Feature; // Ensure this is an Input property
  @Output() featureLoaded = new EventEmitter<any>(); 
  @Input() featureId!: number;
  @Input() featureGeometry!: string; // 'Point', 'Polygon', or 'LineString'

  @Output() featureDeleted = new EventEmitter<number>(); // Emit feature ID
 
 


  editMode = false;
  updatedData: any = {}; // Stores form updates

  constructor(public poiService: PetPointOfInterestService, public dgService: DogParksService, public dwService: DogWalksService) { }


  ngOnInit() {
    console.log("Popup received data:", this.data);
    this.updatedData = { ...this.data }; // Clone data to avoid modifying it directly
  }

  closePopup() {
    this.data = null; // Clear data to hide popup
    this.position = undefined; // Also clears the position to fully remove the popup
  }

  //update
  toggleEdit() {
    this.editMode = !this.editMode;
    this.updatedData = { ...this.data }; // Clone existing data
  }


  saveChanges() {
    if (!this.data || !this.data.id) {
      console.error("Data is undefined or missing an ID:", this.data);
      return;
    }

    console.log("Sending updated data:", this.updatedData);

    let updateObservable;


    // Convert the updated geometry back to WKT
    if (this.updatedData.geometry && this.updatedData.geometry.type) {
      const geoJSONFormat = new GeoJSON();
      const geom = this.updatedData.geometry;

      if (geom.type.toUpperCase() === "POINT") {
        const transformedCoords = toLonLat(geom.coordinates);
        this.updatedData.geometry = `POINT(${transformedCoords[0]} ${transformedCoords[1]})`;
      } else if (geom.type.toUpperCase() === "LINESTRING") {
        const transformedCoords = geom.coordinates.map((coord: [number, number]) =>
          toLonLat(coord)
        );
        this.updatedData.geometry = `LINESTRING(${(transformedCoords as [number, number][]).map((coord) => `${coord[0]} ${coord[1]}`).join(", ")})`;
      } else if (geom.type.toUpperCase() === "POLYGON") {
        const polygonCoords = geom.coordinates[0].map((coord: [number, number]) =>
          toLonLat(coord));
        if (polygonCoords[0][0] !== polygonCoords[polygonCoords.length - 1][0] ||
          polygonCoords[0][1] !== polygonCoords[polygonCoords.length - 1][1]) {
          polygonCoords.push(polygonCoords[0]); // Close polygon if necessary
        }
        this.updatedData.geometry = `POLYGON((${polygonCoords.map((coord: [number, number]) => `${coord[0]} ${coord[1]}`).join(", ")}))`;
      }
    }

    if (this.data.geometry.toLowerCase().includes('polygon')) {
      updateObservable = this.dgService.updateDogPark(this.data.id, this.updatedData);
    } else if (this.data.geometry.toLowerCase().includes('linestring')) {
      updateObservable = this.dwService.updateDogWalk(this.data.id, this.updatedData);
    } else {
      updateObservable = this.poiService.updatePetPoint(this.data.id, this.updatedData);
    }

    updateObservable.subscribe(
      response => {
        console.log('Update successful:', response);
        this.editMode = false;
        this.refreshFeature();
      },
      error => {
        console.error('Error updating:', error);
      }
    );
  }

  
  refreshFeature() {
    if (!this.data || !this.data.id) {
      console.error("Cannot refresh: Data is missing or invalid.");
      return;
    }
  
    let refreshObservable;
    if (this.data.geometry.toLowerCase().includes('polygon')) {
      refreshObservable = this.dgService.getById(this.data.id);
    } else if (this.data.geometry.toLowerCase().includes('linestring')) {
      refreshObservable = this.dwService.getById(this.data.id);
    } else {
      refreshObservable = this.poiService.getById(this.data.id);
    }
  
    refreshObservable.subscribe(
      updatedFeature => {
        console.log("Feature refreshed:", updatedFeature);
  
  
        this.data = updatedFeature; // Update popup data
        this.feature = updatedFeature; // Make sure feature is updated
        this.featureLoaded.emit(updatedFeature); // Emit the updated feature for the map
      },
      error => {
        console.error("Error refreshing feature:", error);
      }
    );
  }


  
  


  onDelete() {
    if (!this.featureId) {
      console.error("No feature ID provided for deletion.");
      return;
    }
  
    console.log(`Attempting to delete feature with ID: ${this.featureId}`);
  
    const geometryType = this.featureGeometry?.toUpperCase(); // Ensure it's in uppercase
    const deletedFeatureId = this.featureId; // Store the ID of the feature being deleted
  
    let deleteObservable;
  
    if (geometryType.includes('POINT')) {
      deleteObservable = this.poiService.deleteById(deletedFeatureId);
    } else if (geometryType.includes('POLYGON')) {
      deleteObservable = this.dgService.deleteById(deletedFeatureId);
    } else if (geometryType.includes('LINESTRING')) {
      deleteObservable = this.dwService.deleteById(deletedFeatureId);
    } else {
      console.error("Unknown feature geometry type:", this.featureGeometry);
      return;
    }
  
    deleteObservable.subscribe({
      next: () => {
        console.log("Feature deleted successfully");
  
        this.featureDeleted.emit(deletedFeatureId); // Emit event with deleted feature ID
        this.closePopup(); // Close popup
        
     
      },
      error: (err) => console.error("Error deleting feature:", err)
    });
  }
  
  

  


  
  

}
