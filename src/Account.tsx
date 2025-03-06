import './App.css';
import logo from './logo.svg';

const Account: React.FunctionComponent = () => {
    let likes = 0;
    // const [state, dispatch] = useReducer(useReducer, initialState);
    // const addFive = () => dispatch({ type: "setCount", value: state.count + 5 });
    return (
    
      <div className="App">
        
        <header className="App-header">
        <p>Register</p>
        <button id="LogoutButton">
            Logout
        </button>
        
        </header>

        <div id="maincontent">
            <p>Current Posts</p>

            <div id='box1'>
                <div id='box1'>
                    <button id='LoginButtion'>
                        ProfilePicture
                    </button>
                    <p>Jeremy(username)</p>
                    
                </div>
                <div id='box1'>
                    <p>10 Likes</p>
                    <button id='LoginButtion'>
                        HeartPicture
                    </button>  
                    
                </div>
                 
            </div>
            
            <hr></hr>
             
            <div id='box1'>
                <div>
                    <p>Post Title</p>
                    <p>Post Description</p>
                    <p>x</p>
                    <p>x</p>
                    <p>x</p>
                    <p>x</p>
                    
                </div>
                <div id='box1'>
                    <img src={logo} className="App-logo" alt="logo" />
                    
                </div>
                 
            </div>

            <hr></hr>

            <p>Comments</p>

            <div id='box1'>
                <div className='subBox'>
                    <div id='box1'>
                        <button id='LoginButton'>
                            ProfilePicture
                        </button>
                        <p>
                            Andy111 <br></br>
                            This is awesome!
                        </p>
                        
                    </div>
                </div>
                
                <div className='subBox'>
                    <div id='box1'>
                        <button id='LoginButton'>
                            ProfilePicture
                        </button>
                        <p>
                            Andy111 <br></br>
                            This is awesome!
                        </p>
                        
                    </div>
                </div>
                 
            </div>
        </div>

        <div id="maincontent">
            <p>Current Posts</p>

            <div id='box1'>
                <div id='box1'>
                    <button id='LoginButtion'>
                        ProfilePicture
                    </button>
                    <p>Jeremy(username)</p>
                    
                </div>
                <div id='box1'>
                    <p>10 Likes</p>
                    <button id='LoginButtion'>
                        HeartPicture
                    </button>  
                    
                </div>
                 
            </div>
            
            <hr></hr>
             
            <div id='box1'>
                <div>
                    <p>Post Title</p>
                    <p>Post Description</p>
                    <p>x</p>
                    <p>x</p>
                    <p>x</p>
                    <p>x</p>
                    
                </div>
                <div id='box1'>
                    <img src={logo} className="App-logo" alt="logo" />
                    
                </div>
                 
            </div>

            <hr></hr>

            <p>Comments</p>

            <div id='box1'>
                <div className='subBox'>
                    <div id='box1'>
                        <button id='LoginButton'>
                            ProfilePicture
                        </button>
                        <p>
                            Andy111 <br></br>
                            This is awesome!
                        </p>
                        
                    </div>
                </div>
                
                <div className='subBox'>
                    <div id='box1'>
                        <button id='LoginButton'>
                            ProfilePicture
                        </button>
                        <p>
                            Andy111 <br></br>
                            This is awesome!
                        </p>
                        
                    </div>
                </div>
                 
            </div>
        </div>
        
      </div>
    );
}

export default Account;