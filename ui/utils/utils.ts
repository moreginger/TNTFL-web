import * as moment from 'moment';
import { Game, Player } from 'tntfl-api';

export function getLadderLeagueClass(rank: number, numActivePlayers: number) {
  let league = '';
  if (rank === -1) {
    league = 'inactive';
  }
  else if (rank === 1) {
    league = 'ladder-first';
  }
  else if (1 < rank && rank <= numActivePlayers * 0.1) {
    league = 'ladder-silver';
  }
  else if (0.1 * numActivePlayers < rank && rank <= numActivePlayers * 0.3) {
    league = 'ladder-bronze';
  }
  return `ladder-position ${league}`;
}

function formatDate(date: moment.Moment) {
  if (date.isBefore(moment().subtract(7, 'days'))) {
    return date.format('YYYY-MM-DD HH:mm');
  }
  else if (date.isBefore(moment().startOf('day'))) {
    return date.format('ddd HH:mm');
  }
  else {
    return date.format('HH:mm');
  }
}

export function formatEpoch(epoch: number) {
  return formatDate(moment.unix(epoch));
}

export function getMonthName(month: number): string {
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];
  return monthNames[month];
}

export function getParameters(num: number): string[] {
  const url = window.location.href;
  const split = url.split('/').filter((s) => s.length > 0);
  return split.slice(split.length - num);
}

export function formatRankChange(rankChange: number): string {
  if (rankChange === 0) {
    return '-';
  }
  return (rankChange > 0 ? '▲' : '▼') + Math.abs(rankChange);
}

export function getNearlyInactiveClass(activity: number): string {
  const isNearlyInactive = activity < 0.25;
  return isNearlyInactive ? 'nearly-inactive' : '';
}

export function mostRecentGames(games: Game[]): Game[] {
  return games.slice(games.length > 5 ? games.length - 5 : 0).reverse();
}

export function skillChange(game: Game, player: Player): number {
  return game.red.name === player.name ? game.red.skillChange : game.blue.skillChange;
}
