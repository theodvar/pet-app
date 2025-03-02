export interface DogParks {
    id: number;
    title: string;
    location: string;
    city: string;
    comment: string;
    geometry: string; // This is a JSON string; you might need to parse it
    image: string | null;
  }