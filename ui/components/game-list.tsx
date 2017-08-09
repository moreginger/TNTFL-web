import * as React from 'react';
import { Component, Props } from 'react';
import { Grid } from 'react-bootstrap';
import { PlayersApi, Game } from 'tntfl-api';

import GameSummary from './game-summary';
import { mapsEqual } from '../utils/utils';

interface GameListProps extends Props<GameList> {
  games: Game[];
  base: string;
}
interface State {
  activePlayers?: Map<number, number>;
}
export default class GameList extends Component<GameListProps, State> {
  constructor(props: GameListProps, context: any) {
    super(props, context);
    this.state = {
      activePlayers: undefined,
    };
  }
  async loadActivePlayers() {
    const { base, games } = this.props;
    if (games.length > 0) {
      const at = games.map((game) => game.date - 1).join(',');
      const json: {[key: string]: {count: number}} = await new PlayersApi(fetch, base).getActive({at});
      const activePlayers = Object.keys(json).reduce((acc, cur) => acc.set(+cur, json[cur].count), new Map<number, number>());
      this.setState({activePlayers});
    }
  }
  componentDidMount() {
    this.loadActivePlayers();
  }
  shouldComponentUpdate(nextProps: GameListProps, nextState: State) {
    return this.props.games !== nextProps.games || !mapsEqual(this.state.activePlayers, nextState.activePlayers);
  }
  componentDidUpdate() {
    this.loadActivePlayers();
  }
  render(): JSX.Element {
    const { games, base } = this.props;
    const { activePlayers } = this.state;
    return (
      <Grid fluid={true}>
        {games.map((game) =>
          <GameSummary
            game={game}
            base={base}
            numActivePlayers={(activePlayers && activePlayers.get(game.date - 1)) || 0}
            key={`${game.date}`}
          />,
        )}
      </Grid>
    );
  }
}
