import { loadFeature, defineFeature } from 'jest-cucumber';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { expect, vi } from 'vitest';
import axios from 'axios';
import ProfileSelection from '../ProfileSelection';

// Mock axios
vi.mock('axios');

const feature = loadFeature('/app/features/ProfileUI.feature', {
    loadRelativePath: false
});

console.log('DEBUG PROFILE FEATURE:', JSON.stringify(feature, null, 2));

console.log('DEBUG PROFILE FEATURE:', JSON.stringify(feature, null, 2));
if (feature.scenarios.length === 0) {
    throw new Error('No scenarios found in feature file!');
}

defineFeature(feature, test => {
    test('Displaying Existing Profiles', ({ given, when, then }) => {
        given(/^the following profiles exist:$/, async (table) => {
            const profiles = table.map(row => ({
                id: row.name === 'Alice' ? 1 : 2,
                name: row.name,
                level: parseInt(row.level),
                score: parseInt(row.score)
            }));
            axios.get.mockResolvedValue({ data: profiles });
        });

        when('I load the profile selection screen', async () => {
            render(<ProfileSelection onSelectProfile={() => { }} />);
        });

        then(/^I should see a profile for "(.*)"$/, async (name) => {
            await waitFor(() => {
                expect(screen.getByText(name)).toBeInTheDocument();
            });
        });
    });

    test('Creating a New Profile', ({ given, when, then }) => {
        given('no profiles exist', async () => {
            axios.get.mockResolvedValue({ data: [] });
            // Mock create response
            axios.post.mockResolvedValue({
                data: { id: 3, name: 'Charlie', level: 3, score: 0 }
            });
        });

        when('I load the profile selection screen', async () => {
            render(<ProfileSelection onSelectProfile={() => { }} />);
            await waitFor(() => expect(screen.getByText('Who is playing?')).toBeInTheDocument());
        });

        when(/^I enter "(.*)" into the new profile input$/, async (name) => {
            const input = screen.getByPlaceholderText('Enter your name...');
            fireEvent.change(input, { target: { value: name } });
        });

        when('I click the create button', async () => {
            const createBtn = screen.getByRole('button', { name: '' });
            fireEvent.click(createBtn);
        });

        then(/^I should see a profile for "(.*)"$/, async (name) => {
            await waitFor(() => {
                expect(screen.getByText(name)).toBeInTheDocument();
            });
        });
    });
});
