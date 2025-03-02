import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DogWalksService {
  private apiUrl = 'http://127.0.0.1:5000/api/dogwalks'; // Flask API endpoint for dogwalks

  constructor(private http: HttpClient) { }



  getDogWalks(): Observable<any> {
    console.log(this.http.get(this.apiUrl))
    return this.http.get(this.apiUrl);
  }

  getById(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }

  // Method to post a new DogWalk
  postLinestring(dwData: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    console.log('Sending POI to API:', dwData);
    return this.http.post(this.apiUrl, dwData, { headers });
  }

  updateDogWalk(id: number, updatedData: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.put(`${this.apiUrl}/${id}`, updatedData, { headers });
  }

  deleteById(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

}

