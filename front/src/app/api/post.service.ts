import { Injectable } from '@angular/core';
import { Observable, of, Subject, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Post} from '../blog/models/post';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseUrl = 'http://localhost:5000/';
  private postSource = new Subject<Post>();

  post$ = this.postSource.asObservable();
  
  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  getPostsInBoard(boardId: number, page: number): Observable<Post[]> {
    let url;

    if (page) {
      url = this.baseUrl + `boards/${boardId}/posts?page=${page}`;
    } else {
      url = this.baseUrl + `boards/${boardId}/posts`;
    }
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>(`getPostsInBoard`, []))
      )
  }

  getPost(idPost: number): Observable<Post> {
    const url = this.baseUrl + `posts/${idPost}`;
    return this.http.get<Post>(url)
    .pipe(
      catchError(this.handleError<Post>(`getPost`))
    )
  }

  createPost(body: any, boardId: number) {
    const url = this.baseUrl + `posts?idBoard=${boardId}`;

    return this.http.post(url, body)
    .pipe(
      catchError(this.handleError<Post>(`createPost`))
    )
  }

  updatePost(body: any, postId: number) {
    const url = this.baseUrl + `posts/${postId}`;
 
    return this.http.patch(url, body)
    .pipe(
      catchError(this.handleError<Post>(`patchPost`))
    )
  }

  deletePost(id: number) {
    const url = this.baseUrl + `posts/${id}`;

    return this.http.delete(url)
    .pipe(
      catchError(this.handleError<Post>(`deletePost`))
    )
  }

  likePost(id: number) {
    const url = this.baseUrl + `posts/${id}/like`;
  
    return this.http.patch(url, '')
    .pipe(
      catchError(this.handleError(`likePost`))
    )
  }

  unlikePost(id: number) {
    const url = this.baseUrl + `posts/${id}/unlike`;

    return this.http.patch(url, '')
    .pipe(
      catchError(this.handleError(`unlikePost`))
    )
  }

  getPostsRank(): Observable<Post[]> {
    const url = this.baseUrl + `posts/rank`;
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>('getPostsRank'))
    )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      let errorMsg = '';
      if (error.error instanceof ErrorEvent) {
        errorMsg = `Error: ${error.error.message}`; 
      } else {
        errorMsg = `Error Code: ${error.status}\nMessage: ${error.message}`
      }
      if(error.status === 401) {
        this.router.navigate(['/member/login'])
      }

      console.error(error);

      window.alert(errorMsg);

      return throwError(errorMsg)

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }), 
  withCredentials: true,
};