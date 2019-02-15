import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule } from "@angular/material/icon";
import { InMemoryDataService } from './services/in-memory-data.service';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BoardListComponent } from './components/board-list/board-list.component';
import { PostListComponent } from './components/post-list/post-list.component';

@NgModule({
  declarations: [
    AppComponent,
    BoardListComponent,
    PostListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false}
    ),
    MatIconModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
