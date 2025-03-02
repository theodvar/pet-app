import { Component, AfterViewInit, ElementRef, ViewChild, OnDestroy, Input, EventEmitter } from '@angular/core';
import Map from 'ol/Map.js';
import View from 'ol/View.js';
import Draw from 'ol/interaction/Draw.js';
import TileLayer from 'ol/layer/Tile.js';
import VectorLayer from 'ol/layer/Vector.js';
import OSM from 'ol/source/OSM.js';
import VectorSource from 'ol/source/Vector.js';
import Geometry from 'ol/geom/Geometry.js';
import { PetPointOfInterestService } from '../services/petpointofinterest.service';
import { DogParksService } from '../services/dogparks.service';
import { DogWalksService } from '../services/dogwalks.service';
import GeoJSON from 'ol/format/GeoJSON';
import { fromLonLat, toLonLat } from 'ol/proj';
import { Feature } from 'ol';
import { MapControlsComponent } from '../map-controls/map-controls.component';
import { Subject, takeUntil } from 'rxjs'; // Import Subject and operators
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PopupComponent } from '../popup/popup.component';
import { Transform } from 'ol/transform';
import { Modify } from 'ol/interaction';
import { defaults as defaultInteractions } from 'ol/interaction/defaults.js';
import Select from 'ol/interaction/Select.js';


enum GeometryType {
  Point = 'Point',
  LineString = 'LineString',
  Polygon = 'Polygon',
  None = 'None',
  // ... other geometry types
}

@Component({
  selector: 'app-draw-features',
  imports: [CommonModule, MapControlsComponent, FormsModule, PopupComponent// Import your MapComponent
  ],
  templateUrl: './draw-features.component.html',
  styleUrls: ['./draw-features.component.css']
})



export class DrawFeaturesComponent implements AfterViewInit, OnDestroy {
  @ViewChild('mapElement', { static: false }) mapElement!: ElementRef;
  @ViewChild(MapControlsComponent) mapControlsComponent!: MapControlsComponent; // Get reference to child component
  @ViewChild(PopupComponent) popupComponent!: PopupComponent; //popup
  @Input() PopupComponent!: PopupComponent; // Ensure PopupComponent is injected
 
 



  private map!: Map;
  private destroy$ = new Subject<void>(); // Subject to track component destruction
  private source = new VectorSource({ wrapX: false });
  private draw!: Draw;
  private transform!: Transform;

  popupData: any = null; //popup
  popupPosition: number[] | undefined = undefined; //popup




  showForm: boolean = false; // Flag to control form visibility
  drawnGeometryWKT: string = ''; // Store WKT geometry
  poiData: any = { name: '', category: '', address: '', city: '', comment: '' }; // Form data for points
  dwData: any = { title: '', location: '', city: '', comment: '' }; // Form data for linestrings and polygons


  // Dropdown-related properties
  drawTypes: GeometryType[] = [GeometryType.None, GeometryType.Point, GeometryType.LineString, GeometryType.Polygon];
  selectedDrawType: string = GeometryType.None; // Default selection

  constructor(public poiService: PetPointOfInterestService, public dgService: DogParksService, public dwService: DogWalksService) { }

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
    return this.getLabel(this.selectedDrawType);
  }

  onFeatureDeleted(featureId: number) {
    console.log("Removing feature from map with ID:", featureId);
  
    // Find the feature in the map layer source
    const source = this.source;
    const feature = source.getFeatureById(featureId);
  
    if (feature) {
      source.removeFeature(feature);
      console.log("Feature removed from map:", feature);
    } else {
      console.warn("Feature not found in source, possibly already removed.");
    }
  }


  ngAfterViewInit(): void {
    const select = new Select({
    });



    const modify = new Modify({
      features: select.getFeatures(),
    });


    this.map = new Map({
      interactions: defaultInteractions().extend([select, modify]),
      target: 'map', // The HTML element ID where the map is rendered
      layers: [
        new TileLayer({
          source: new OSM() // OpenStreetMap base layer
        }),
        new VectorLayer({ source: this.source })
      ],
      view: new View({
        center: fromLonLat([23.7056575, 37.9784828]), // Centered in Athens
        zoom: 12
      })
    });

    this.map.addInteraction(select);
    this.map.addInteraction(modify);

    // Listen for geometry modifications
    modify.on('modifyend', (event) => {
      const modifiedFeature = event.features.item(0) as Feature;
      const geoJSONFormat = new GeoJSON();
      const updatedGeoJSON = geoJSONFormat.writeFeatureObject(modifiedFeature);

      console.log("Modified Geometry (GeoJSON):", updatedGeoJSON);

      if (this.popupComponent && this.popupComponent.data) {
        this.popupComponent.updatedData.geometry = updatedGeoJSON.geometry;
        console.log("Updated data in Popup:", this.popupComponent.updatedData);
      }
    });



    // Add click event to the map

    this.map.on('click', (event) => {
      
      const feature = this.map.forEachFeatureAtPixel(event.pixel, (feat) => feat);
      if (feature) {
        const properties = feature.getProperties();

        console.log('Feature properties:', properties); // Debugging
        console.log('Geometry:', properties['geometry']); // Debugging

        if (!properties['id']) {
          console.log('New feature clicked, ignoring popup');
          return; // Ignore new, unsaved features
        }

        // Convert OpenLayers geometry to GeoJSON
        const geoJSONFormat = new GeoJSON();
        let geometryType = '';

        if (properties['geometry']) {
          try {
            const geoJSONGeometry = geoJSONFormat.writeGeometryObject(properties['geometry']);
            geometryType = geoJSONGeometry.type.toLowerCase(); // Normalize to lowercase
            console.log('Converted Geometry Type:', geometryType);
          } catch (error) {
            console.error('Error converting geometry to GeoJSON:', error);
            return;
          }
        } else {
          console.error('Invalid or missing geometry:', properties['geometry']);
          return;
        }

        // Determine which API to call based on geometry type
        if (geometryType.startsWith('polygon')) {
          this.dgService.getById(properties['id']).subscribe(
            (data) => {
              console.log('Fetched data (Polygon):', data);
              this.popupData = data;
              this.popupPosition = [event.pixel[0], event.pixel[1]];
            },
            (error) => console.error('Error fetching polygon data:', error)
          );
        } else if (geometryType.startsWith('linestring')) {
          this.dwService.getById(properties['id']).subscribe(
            (data) => {
              console.log('Fetched data (LineString):', data);
              this.popupData = data;
              this.popupPosition = [event.pixel[0], event.pixel[1]];
            },
            (error) => console.error('Error fetching linestring data:', error)
          );
        } else {
          this.poiService.getById(properties['id']).subscribe(
            (data) => {
              console.log('Fetched data (Point or default):', data);
              this.popupData = data;
              this.popupPosition = [event.pixel[0], event.pixel[1]];
            },
            (error) => console.error('Error fetching point data:', error)
          );
        }

      } else {
        this.popupData = null;
        this.popupPosition = undefined;
      }

    });

    




    // Subscribe to mapInitialized event from MapControlsComponent
    if (this.mapControlsComponent) { // Check if the component is available
      this.mapControlsComponent.mapInitialized.pipe(takeUntil(this.destroy$)).subscribe(() => {
        console.log('Map is initialized!');
      });
    } else {
      console.error("mapControlsComponent is not available yet.");
    }
  }

  
  addFeatureLayer(layer: VectorLayer): void {
    if (this.map) {
      this.map.addLayer(layer);
    } else {
      console.error('Map is not initialized yet.');
    }
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    if (this.draw) {
      this.map.removeInteraction(this.draw);

    }
    if (this.map) {
      this.map.dispose();
    }
  }


  // Handle dropdown selection
  selectDrawType(type: GeometryType): void {
    this.selectedDrawType = type;
    this.removeInteraction();
    this.addInteraction(type);
  }

  drawnGeometryGeoJSON: any = null; // Variable to store GeoJSON
  selectedGeometryType: string = ''; // Store current geometry type


  private addInteraction(type: GeometryType): void {
    if (type !== GeometryType.None) {
      this.draw = new Draw({
        source: this.source,
        type: type
      });

      this.draw.on('drawend', (event) => {
        const feature = event.feature as Feature<Geometry>;
        feature.setProperties({ isNew: true }); // Ensure isNew is stored
        console.log('New feature drawn:', feature.getProperties());
        console.log('Features in source after draw:', this.source.getFeatures().map(f => f.getProperties()));

        const format = new GeoJSON();
        this.drawnGeometryGeoJSON = format.writeFeatureObject(feature);
        console.log('Drawn GeoJSON:', this.drawnGeometryGeoJSON);

        const geom = this.drawnGeometryGeoJSON.geometry;
        const geometryType = geom.type;
        const coordinates = geom.coordinates;

        console.log('geometryType:', geometryType);
        console.log('coordinates:', coordinates);

        this.selectedGeometryType = geom.type.toUpperCase(); // Store geometry type


        if (geometryType.toUpperCase() === "POINT") {
          // POINT(x y)
          const transformedCoords = toLonLat(coordinates);
          this.drawnGeometryWKT = `POINT(${transformedCoords[0]} ${transformedCoords[1]})`;
        } else if (geometryType.toUpperCase() === "LINESTRING") {

          // LINESTRING(x1 y1, x2 y2, x3 y3, ...)
          const transformedCoords = coordinates.map((coord: [number, number]) =>
            toLonLat(coord)
          );
          this.drawnGeometryWKT = `LINESTRING(${(transformedCoords as [number, number][]).map((coord) => `${coord[0]} ${coord[1]}`).join(", ")})`;

        } else if (geometryType.toUpperCase() === "POLYGON") {
          // POLYGON((x1 y1, x2 y2, x3 y3, ..., x1 y1))
          const polygonCoords = coordinates[0].map((coord: [number, number]) =>
            toLonLat(coord)); // Extract first array
          if (polygonCoords[0][0] !== polygonCoords[polygonCoords.length - 1][0] ||
            polygonCoords[0][1] !== polygonCoords[polygonCoords.length - 1][1]) {
            polygonCoords.push(polygonCoords[0]); // Close polygon if necessary
          }
          this.drawnGeometryWKT = `POLYGON((${polygonCoords.map((coord: [number, number]) => `${coord[0]} ${coord[1]}`).join(", ")}))`;
        }

        console.log('WKT Geometry:', this.drawnGeometryWKT);

        // Show the form for user input
        this.showForm = true;



      });


      this.map.addInteraction(this.draw);

    }
  }


  refreshLayer(layerName: string) {
    const layers = this.map.getLayers().getArray();
    const targetLayer = layers.find(layer => layer.get('name') === layerName);
  
    if (targetLayer instanceof VectorLayer) {
      const source = targetLayer.getSource() as VectorSource;
      source.clear(); // Clear existing features
  
      let fetchService;
      if (layerName === 'petpointofinterest') {
        fetchService = this.poiService.getPoints();
      } else if (layerName === 'dogwalk') {
        fetchService = this.dwService.getDogWalks;
      } else if (layerName === 'dogpark') {
        fetchService = this.dgService.getDogParks();
      }
  
      if (typeof fetchService === 'function') {
        fetchService().subscribe((features :any) => {
          source.addFeatures(new GeoJSON().readFeatures(features, {
            featureProjection: 'EPSG:3857',
          }));
        });
      }
    }
  }
  




  submitForm(): void {
    console.log('Features in source before submission:', this.source.getFeatures().map(f => f.getProperties()));
    if (!this.drawnGeometryWKT) {
      console.error('No geometry to submit');
      return;
    }

    // Combine form data with geometry
    let finalData;

    if (this.drawnGeometryWKT.startsWith("POINT")) {
      finalData = { ...this.poiData, geometry: this.drawnGeometryWKT };
    } else {
      finalData = { ...this.dwData, geometry: this.drawnGeometryWKT };
    }
    console.log('Submitting:', finalData);

    // Send to API
    if (this.drawnGeometryWKT.startsWith("POINT")) {
      this.poiService.postPoint(finalData).subscribe(
        response => {
          console.log('API Response:', response);
          this.showForm = false; // Hide form after submission
          this.poiData = { name: '', category: '', address: '', city: '', comment: '' }; // Reset form
        },
        error => console.error('Error submitting:', error)
      );
    } else if (this.drawnGeometryWKT.startsWith("LINE")) {
      this.dwService.postLinestring(finalData).subscribe( // Assuming a different endpoint
        response => {
          console.log('API Response:', response);
          this.showForm = false; // Hide form after submission
          this.dwData = { title: '', location: '', city: '', comment: '' }; // Reset form
        },
        error => console.error('Error submitting:', error)
      );
    } else {
      this.dgService.postPolygon(finalData).subscribe( // Assuming a different endpoint
        response => {
          console.log('API Response:', response);
          this.showForm = false; // Hide form after submission
          this.dwData = { title: '', location: '', city: '', comment: '' }; // Reset form
        },
        error => console.error('Error submitting:', error)
      );
    }
  }


  private removeInteraction(): void {
    if (this.draw) {
      this.map.removeInteraction(this.draw);
    }
  }

  undo(): void {
    if (this.draw) {
      this.draw.removeLastPoint();
    }
  }

  openPopup(featureData: any) {
    this.popupData = featureData; // Triggers popup in the left panel
  }

  closePopup() {
    this.popupData = null; // Hides popup when closed
  }

  

  handleFeatureDeleted() {
    // Refresh map data or reload the source here.
    console.log("Feature deleted. Refreshing the map...");
    
  }

  ngOnInit() {
    // Do not call the API here
  }

  loadMapData(): void {
    // Load Points
    this.poiService.getPoints().subscribe((features: any) => {
      const vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: new GeoJSON().readFeatures(features, { featureProjection: 'EPSG:3857' }),
        }),
      });
      vectorLayer.set('name', 'petpointofinterest');
      this.map.addLayer(vectorLayer);
    });
  
    // Load Dogwalks
    this.dwService.getDogWalks().subscribe((features: any) => {
      const vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: new GeoJSON().readFeatures(features, { featureProjection: 'EPSG:3857' }),
        }),
      });
      vectorLayer.set('name', 'dogwalk');
      this.map.addLayer(vectorLayer);
    });
  
    // Load Dogparks
    this.dgService.getDogParks().subscribe((features: any) => {
      const vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: new GeoJSON().readFeatures(features, { featureProjection: 'EPSG:3857' }),
        }),
      });
      vectorLayer.set('name', 'dogpark');
      this.map.addLayer(vectorLayer);
    });
  }
  


refreshMap(): void {
  if (!this.map) {
    console.error("Map is not initialized yet.");
    return;
  }

  // Clear all vector sources
  const layers = this.map.getLayers().getArray();
  layers.forEach((layer) => {
    if (layer instanceof VectorLayer) {
      const source = layer.getSource();
      if (source instanceof VectorSource) {
        source.clear();
      }
    }
  });

  // Reload data from APIs
  this.loadMapData();
}


  
  

}