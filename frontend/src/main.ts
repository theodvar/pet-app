import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http'; 
import { appConfig } from './app/app.config';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient(), provideAnimationsAsync()], 
}).catch(err => console.error(err)); 