import { Component } from '@angular/core';
//import { MapComponent } from './map/map.component';
import { DrawFeaturesComponent } from './draw-features/draw-features.component';
import { MapControlsComponent } from './map-controls/map-controls.component';
import { AboutPageComponent } from './about-page/about-page.component';







@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    DrawFeaturesComponent,
    MapControlsComponent,// Import your MapComponent
    AboutPageComponent
  ],
  // providers: [provideHttpClient()], // Add provideHttpClient() to providers
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'openlayers-demo';
}