import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Comment } from '../models/comment';

@Injectable({
  providedIn: 'root'
})

export class InMemoryDataService implements InMemoryDbService{
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

    const users = [
      { id: 1, full_name: '루카', email: 'test@test.com' },
      { id: 2, full_name: '루카', email: 'test@test.com' },
      { id: 3, full_name: '루카', email: 'test@test.com' },
      { id: 4, full_name: '루카', email: 'test@test.com' },
      { id: 5, full_name: '루카', email: 'test@test.com' },
      { id: 6, full_name: '루카', email: 'test@test.com' },
    ]

    const posts = [
      { id: 1, board_id: 1, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: 'GSAT 시각적사고 도서 질문이요~~'},
      { id: 2, board_id: 1, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '전자공학과 스펙 질문' },
      { id: 3, board_id: 2, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '명지대 자연과학vs가톨릭대 미디어기술콘텐츠' },
      { id: 4, board_id: 2, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '대학교 2학년' },
      { id: 5, board_id: 2, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '경영 복전!!' },
      { id: 6, board_id: 3, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '학점관리 좀 열심히 할 것 그랬어요. ' },
      { id: 7, board_id: 3, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '다들 동아리활동 어떤거 하시나요' },
      { id: 8, board_id: 3, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: true, title: '학점 3.68과 3.73의 차이는 있습니까?' },
      { id: 9, board_id: 3, like_count: 10, view_count: 10, body: '<h1>Test header</h1> <p>test paragraph</p>', created_at: '2019.01.01', writer: users[0], has_image: false, title: '기계공학과 4학년 노답인데 도대체 어떻게 풀어나가야 할까요ㅠㅠ'},
    ];

    const comments =[
      { id: 1, idPost: 1, idParentComment: 1, body: '테스트 댓글', path:'000001', writer: users[0], createdAt: '2019.01.01', updatedAt: '2019.01.01' },
      { id: 2, idPost: 1, idParentComment: 1, body: '테스트 댓글', path:'000001', writer: users[0], createdAt: '2019.01.01', updatedAt: '2019.01.01' },
      { id: 3, idPost: 2, idParentComment: 1, body: '테스트 댓글', path:'000001', writer: users[0], createdAt: '2019.01.01', updatedAt: '2019.01.01' },
      { id: 4, idPost: 2, idParentComment: 1, body: '테스트 댓글', path:'000001', writer: users[0], createdAt: '2019.01.01', updatedAt: '2019.01.01' },
      { id: 5, idPost: 3, idParentComment: 1, body: '테스트 댓글', path:'000001', writer: users[0], createdAt: '2019.01.01', updatedAt: '2019.01.01' },
    ]

    return {boards, posts, users, comments};
    
  }

  genId(comments: Comment[]): number {
    return comments.length > 0 ? Math.max(...comments.map(comment => comment.id)) + 1: 11;
  }

  constructor() { }
}
