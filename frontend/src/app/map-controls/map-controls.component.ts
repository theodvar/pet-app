import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { PetPointOfInterestService } from '../services/petpointofinterest.service';
import { DogParksService } from '../services/dogparks.service';
import { DogWalksService } from '../services/dogwalks.service';
import GeoJSON from 'ol/format/GeoJSON';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { CommonModule } from '@angular/common';




@Component({
  selector: 'app-map-controls',
  standalone: true,
  imports:[CommonModule],
  templateUrl: './map-controls.component.html',
  styleUrls: ['./map-controls.component.css']
})
export class MapControlsComponent implements OnInit{

  geometryTypes = ['None', 'Point', 'LineString', 'Polygon'];

  selectedGeometry= 'None'; // Set default value

  @Output() featureLoaded = new EventEmitter<VectorLayer>();
  @Output() mapInitialized = new EventEmitter<void>(); // New output
  

  constructor(
    public poiService: PetPointOfInterestService, 
    public dgService: DogParksService, 
    public dwService: DogWalksService) { }
  
    ngOnInit(): void { // Initialize
      this.loadFeatures(); // Load initial features
    }

    getLabel(type: string): string {
      switch (type) {
        case 'Point':
          return 'Point of Pet Interest';
        case 'Polygon':
          return 'Dogpark';
        case 'LineString':
          return 'Dogwalk';
        default:
          return type;
      }
    }
  
    get selectedLabel(): string {
      return this.getLabel(this.selectedGeometry);
    }

    selectGeometry(type: string) {
      this.selectedGeometry = type;
      console.log(`Selected Geometry: ${type}`);
      this.loadFeatures(); // Call loadFeatures without parameter
    }

    loadFeatures() {
      console.log("Loading features for:", this.selectedGeometry);

      const emptyLayer = new VectorLayer({ source: new VectorSource() });
      this.featureLoaded.emit(emptyLayer); // Clear previous features
  

      switch (this.selectedGeometry) {
        case 'Point':
          this.loadPoints();
          break;
        case 'Polygon':
          this.loadPolygons();
          break;
        case 'LineString':
          this.loadLineStrings();
          break;
        default: // Handle 'None' or other cases
          //  Clear the map or do nothing
          this.featureLoaded.emit(emptyLayer); // Emit an empty layer
          break;
      }
    }

    loadPoints(): void {

      this.poiService.getPoints().subscribe({
        next: (geojsonData) => {
          const vectorLayer = this.createVectorLayer(geojsonData);
          this.featureLoaded.emit(vectorLayer);
        },
        error: (err) => console.error('Error loading points:', err)
      });
    }

    loadPolygons(): void {

      this.dgService.getDogParks().subscribe({
        next: (geojsonData) => {
          const vectorLayer = this.createVectorLayer(geojsonData);
          this.featureLoaded.emit(vectorLayer);
        },
        error: (err) => console.error('Error loading polygons:', err)
      });
    }

    loadLineStrings(): void {

      this.dwService.getDogWalks().subscribe({
        next: (geojsonData) => {
          const vectorLayer = this.createVectorLayer(geojsonData);
          this.featureLoaded.emit(vectorLayer);
        },
        error: (err) => console.error('Error loading linestrings:', err)
      });
    }

    private createVectorLayer(geojsonData: any): VectorLayer {
      const vectorSource = new VectorSource({
        features: new GeoJSON().readFeatures(geojsonData, {
          featureProjection: 'EPSG:3857',
        }),
      });
      return new VectorLayer({ source: vectorSource });
    }

 
    // clearMap() {
    //   console.log("Clearing map...");
    //   const emptyLayer = new VectorLayer({ source: new VectorSource() });
    //   this.featureLoaded.emit(emptyLayer); // Emit an empty layer to clear the map
    // }


}
