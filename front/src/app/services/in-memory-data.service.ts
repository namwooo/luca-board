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

    const posts = [
      { id: 1, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: 'GSAT 시각적사고 도서 질문이요~~'},
      { id: 2, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '전자공학과 스펙 질문' },
      { id: 3, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '명지대 자연과학vs가톨릭대 미디어기술콘텐츠' },
      { id: 4, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '대학교 2학년' },
      { id: 5, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '경영 복전!!' },
      { id: 6, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '학점관리 좀 열심히 할 것 그랬어요. ' },
      { id: 7, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '다들 동아리활동 어떤거 하시나요' },
      { id: 8, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: true, title: '학점 3.68과 3.73의 차이는 있습니까?' },
      { id: 9, like_count: 10, view_count: 10, created_at: '2019.01.01', writer: { name: '루카' }, has_image: false, title: '기계공학과 4학년 노답인데 도대체 어떻게 풀어나가야 할까요ㅠㅠ'},
    ]; 
    return {boards, posts};
    
  }

  constructor() { }
}
