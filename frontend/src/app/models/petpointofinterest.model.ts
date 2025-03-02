export interface PetPointOfInterest {
    id: number;
    name: string;
    address: string;
    category: string;
    city: string;
    comment: string;
    geometry: string; // This is a JSON string; you might need to parse it
    image: string | null;
  }