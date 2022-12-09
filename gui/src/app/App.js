import React from 'react';
import {QueryClient, QueryClientProvider} from 'react-query';

import Page from './Page';

import './App.css'

function App() {
    const queryClient = new QueryClient()

	return (
		<div className='App-root'>
            <QueryClientProvider client={queryClient}>
                <Page />
            </QueryClientProvider>
		</div>
	);
}

export default App