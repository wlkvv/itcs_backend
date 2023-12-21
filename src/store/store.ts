import {configureStore} from "@reduxjs/toolkit";
import { combineReducers } from 'redux';

import authReducer from "./users/authSlice"
import cartReducer from '/home/student/labs_4/lab_6/src/store/cartSlice.ts';
import loginReducer from "./users/loginSlice"
import registerReducer from "./users/registerSlice"
import searchReducer from "./searchSlice";
import ordersReducer from "./ordersSlice";


export interface RootState {
	user: {
	  user_id: BigInteger;
	  user_email: string;
	  is_authenticated: boolean;
	  is_moderator: boolean;
	  current_cart: number;
	  cart: ReturnType<typeof cartReducer>;
	};
	search: { // Добавьте новое состояние для поиска
	  query: string;
	};
  }
  
  export const store = configureStore({
	reducer: {
	  user: authReducer,
	  login: loginReducer,
	  //order: orderReducer,
	  //cart: cartReducer,
	  //service: serviceReducer,
	  register: registerReducer,
	  cart: cartReducer,
	  orders: ordersReducer,
	  search: searchReducer, // Добавьте новый редьюсер в хранилище
	},
  });
  
  export default store;
  export type AppDispatch = typeof store.dispatch;