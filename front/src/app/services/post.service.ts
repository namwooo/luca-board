import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError} from 'rxjs/operators';

import { Post, PostForm} from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private postUrl = 'http://0.0.0.0:5000/';
  private postSource = new Subject<Post>();

  post$ = this.postSource.asObservable();
  
  constructor(
    private http: HttpClient
  ) { }

  getPostsInBoard(idBoard: number): Observable<Post[]> {
    const url = this.postUrl + `boards/${idBoard}/posts`;
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>(`getPostsInBoard`, []))
      )
  }

  getPost(post_id: number): Observable<Post> {
    const url = this.postUrl + `/${post_id}`;
    return this.http.get<Post>(url)
    .pipe(
      catchError(this.handleError<Post>(`getPost`))
    )
  }

  createPost(postForm: PostForm) {
    return this.http.post(this.postUrl, postForm)
    .pipe(
      catchError(this.handleError<Post>(`createPost`))
    )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};