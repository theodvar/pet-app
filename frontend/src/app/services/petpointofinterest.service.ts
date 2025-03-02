  import { Injectable } from '@angular/core';
  import { HttpClient, HttpHeaders } from '@angular/common/http';
  import { Observable } from 'rxjs';

  @Injectable({
    providedIn: 'root',
  })
  export class PetPointOfInterestService {
    private apiUrl = 'http://127.0.0.1:5000/api/petpointofinterest'; // Flask API endpoint for petspointofnterest

    constructor(private http: HttpClient) {}

    getPoints(): Observable<any> {
      console.log(this.http.get(this.apiUrl))
      return this.http.get(this.apiUrl);
    }

    getById(id: number): Observable<any> {
      return this.http.get(`${this.apiUrl}/${id}`);
    }

    // Method to post a new POI
    postPoint(poiData: any): Observable<any> {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      console.log('Sending POI to API:', poiData);
      return this.http.post(this.apiUrl, poiData, { headers });
    }

    updatePetPoint(id: number, updatedData: any): Observable<any> {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      return this.http.put(`${this.apiUrl}/${id}`, updatedData, { headers });
    }

    deleteById(id: number): Observable<any> {
      return this.http.delete(`${this.apiUrl}/${id}`);
    }
  }

