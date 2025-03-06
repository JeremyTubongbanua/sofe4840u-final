import logo from './logo.svg';
import placeholder from './Placeholder.jpg'
import {useReducer} from 'react';

interface State {
    count: number 
    
 };

const initialState: State = { count: 0 };



const Main: React.FunctionComponent = () => {
    let likes = 0;
    // const [state, dispatch] = useReducer(useReducer, initialState);
    // const addFive = () => dispatch({ type: "setCount", value: state.count + 5 });
    return (
    
      <div className="App">
        
        <div>
          
          <header className="App-header">
          
            <p>Login</p>
            <input type='text' placeholder='Username'></input>
            <input type='text' placeholder='Private Key'></input>
            <button id='LoginButtion'>
                Login Button
            </button>
            <button id='RegisterButton'>
                Go to Register
            </button>

          
            {/* <img src={placeholder} className="App-logo" alt="logo" />
            <p>
              Enter a comment here!
            </p>
  
            <button id='LikeButton' onClick={()=>{likes+=1;}}>
            Like
            </button>
            <p>
              Likes {likes}
            </p>
  
            <button id='LikeButton'>
              Upload picture
            </button> */}
            
          </header>
  
  
          
        </div>
      </div>
    );
}

export default Main;
