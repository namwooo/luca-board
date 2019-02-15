import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InMemoryDataService {
  createDb() {
    const boards = [
      { id: 1, title: '서류합격스펙' },
      { id: 2, title: '합격자소서' },
      { id: 3, title: '인적성 필기후기' },
      { id: 4, title: '면접후기' },
      { id: 5, title: '최종합격스펙' },
      { id: 6, title: '최종합격후기' },
      { id: 7, title: '공채속보' },
      { id: 8, title: '채용공고' },
      { id: 9, title: '중견중소' },
      { id: 10, title: '인턴공고' }
    ];
    return {boards};
  }

  constructor() { }
}
