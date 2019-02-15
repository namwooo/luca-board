import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InMemoryDataService {
  createDb() {
    const boards = [
      { id: 1, title: 'Company life' },
      { id: 2, title: 'Recruit' },
      { id: 3, title: 'Blue Whale' },
      { id: 4, title: 'University' },
      { id: 5, title: 'Wanted' },
      { id: 6, title: 'News' },
      { id: 7, title: 'Employee' },
      { id: 8, title: 'Employer' },
      { id: 9, title: 'Trend' },
      { id: 10, title: 'Money' }
    ];
    return {boards};
  }

  constructor() { }
}
